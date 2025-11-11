"""
Intelligent Auction Bot with Phase-Based Bidding Strategy
"""
import random
import logging
from django.utils import timezone
from django.db import transaction
from django.conf import settings
from .models import Auction, Bid, AuctionLog

logger = logging.getLogger('auctions')


class AuctionBot:
    """Smart auction bot with phase-based bidding strategy."""
    
    def __init__(self, auction):
        self.auction = auction
        self.config = settings.AUCTION_CONFIG
        self.bid_increments = self.config['BID_INCREMENTS']
    
    def can_bid(self):
        """Check if bot can place a bid."""
        if not self.auction.bot_active:
            return False
        
        if self.auction.status != 'active':
            return False
        
        # Check if bot has reached max bid
        if self.auction.bot_current_bid >= self.auction.max_bid:
            return False
        
        # Check if auction has time remaining or can be extended
        if self.auction.remaining_time <= 0 and self.auction.current_phase != 3:
            return False
        
        return True
    
    def get_next_bid_amount(self):
        """Calculate the next bid amount."""
        current = float(self.auction.current_price)
        max_bid = float(self.auction.max_bid)
        bot_current = float(self.auction.bot_current_bid)
        
        # Choose a random increment
        increment = random.choice(self.bid_increments)
        next_bid = current + increment
        
        # Ensure we don't exceed max_bid
        if next_bid > max_bid:
            next_bid = max_bid
        
        # Ensure we don't exceed bot's current bid limit
        if next_bid > bot_current + max(self.bid_increments):
            next_bid = min(next_bid, bot_current + max(self.bid_increments))
        
        return next_bid
    
    def should_bid_in_phase_1(self, elapsed_time, phase_duration):
        """Determine if bot should bid in Phase 1."""
        wait_percentage = self.config['WAIT_PERCENTAGE']
        wait_time = phase_duration * wait_percentage
        
        # Wait 75% of Phase 1
        if elapsed_time < wait_time:
            return False
        
        # Check if human has bid recently (within last 5 seconds)
        recent_human_bid = self.auction.bids.filter(
            bidder_type='human',
            timestamp__gte=timezone.now() - timezone.timedelta(seconds=5)
        ).exists()
        
        if recent_human_bid:
            # React to human bid with delay
            return True
        
        # If no human bid, bid once in last 25% of phase
        if elapsed_time >= wait_time:
            # Check if bot has already bid in this phase
            phase_bids = self.auction.bids.filter(
                bidder_type='bot',
                phase=1
            ).exists()
            
            if not phase_bids:
                return True
        
        return False
    
    def should_bid_in_phase_2(self, elapsed_time, phase_start, phase_duration):
        """Determine if bot should bid in Phase 2."""
        wait_percentage = self.config['WAIT_PERCENTAGE']
        phase_elapsed = elapsed_time - phase_start
        wait_time = phase_duration * wait_percentage
        
        # Wait 75% of Phase 2
        if phase_elapsed < wait_time:
            return False
        
        # Check if human has bid recently
        recent_human_bid = self.auction.bids.filter(
            bidder_type='human',
            timestamp__gte=timezone.now() - timezone.timedelta(seconds=5)
        ).exists()
        
        if recent_human_bid:
            return True
        
        # If no human bid, bid once in last 25% of phase
        if phase_elapsed >= wait_time:
            phase_bids = self.auction.bids.filter(
                bidder_type='bot',
                phase=2
            ).exists()
            
            if not phase_bids:
                return True
        
        return False
    
    def should_bid_in_phase_3(self):
        """Determine if bot should bid in Phase 3 (30% chance per second)."""
        probability = self.config['PHASE_3_BID_PROBABILITY']
        return random.random() < probability
    
    def get_reaction_delay(self):
        """Get random reaction delay for bot."""
        min_delay = self.config['BOT_REACTION_DELAY_MIN']
        max_delay = self.config['BOT_REACTION_DELAY_MAX']
        return random.uniform(min_delay, max_delay)
    
    def place_bid(self, phase=None):
        """Place a bid on behalf of the bot."""
        if not self.can_bid():
            return False
        
        with transaction.atomic():
            # Refresh auction from database
            self.auction.refresh_from_db()
            
            if not self.can_bid():
                return False
            
            # Calculate next bid amount
            next_bid = self.get_next_bid_amount()
            
            # Check if we can afford it
            if next_bid > self.auction.max_bid:
                return False
            
            # Determine phase if not provided
            if phase is None:
                phase = self.auction.current_phase
            
            # Create the bid
            bid = Bid.objects.create(
                auction=self.auction,
                bidder=None,
                bidder_type='bot',
                amount=next_bid,
                phase=phase
            )
            
            # Update auction
            self.auction.current_price = next_bid
            self.auction.bot_current_bid = next_bid
            
            # Extend time in Phase 3 if needed
            if phase == 3 and self.auction.remaining_time <= 5:
                extension_time = self.config['PHASE_3_EXTENSION_TIME']
                if self.auction.end_time:
                    self.auction.end_time += timezone.timedelta(seconds=extension_time)
                    self.auction.extended_time += extension_time
            
            self.auction.save()
            
            # Create log
            AuctionLog.objects.create(
                auction=self.auction,
                event_type='bot_action',
                message=f"Bot placed bid: ₹{next_bid} in Phase {phase}",
                metadata={'amount': float(next_bid), 'phase': phase}
            )
            
            logger.info(f"Bot bid placed: ₹{next_bid} on auction {self.auction.id} in Phase {phase}")
        
        return True
    
    def process_phase_1(self, elapsed_time, phase_duration):
        """Process Phase 1 bidding logic."""
        if self.should_bid_in_phase_1(elapsed_time, phase_duration):
            # Check for recent human bid
            recent_human_bid = self.auction.bids.filter(
                bidder_type='human',
                timestamp__gte=timezone.now() - timezone.timedelta(seconds=5)
            ).first()
            
            if recent_human_bid:
                # React with delay (handled by task scheduler)
                return 'react'
            else:
                # Place bid immediately
                return self.place_bid(phase=1)
        
        return False
    
    def process_phase_2(self, elapsed_time, phase_start, phase_duration):
        """Process Phase 2 bidding logic."""
        if self.should_bid_in_phase_2(elapsed_time, phase_start, phase_duration):
            recent_human_bid = self.auction.bids.filter(
                bidder_type='human',
                timestamp__gte=timezone.now() - timezone.timedelta(seconds=5)
            ).first()
            
            if recent_human_bid:
                return 'react'
            else:
                return self.place_bid(phase=2)
        
        return False
    
    def process_phase_3(self):
        """Process Phase 3 bidding logic."""
        if self.should_bid_in_phase_3():
            return self.place_bid(phase=3)
        
        return False
    
    def check_and_complete(self):
        """Check if auction should be completed."""
        if self.auction.status != 'active':
            return
        
        # Check if bot reached max bid
        if self.auction.bot_current_bid >= self.auction.max_bid:
            self.complete_auction()
            return
        
        # Check if time expired (only if not in Phase 3 or can't extend)
        if self.auction.remaining_time <= 0:
            if self.auction.current_phase != 3:
                self.complete_auction()
            elif self.auction.bot_current_bid >= self.auction.max_bid:
                self.complete_auction()
    
    def complete_auction(self):
        """Complete the auction and determine winner."""
        with transaction.atomic():
            self.auction.refresh_from_db()
            
            if self.auction.status != 'active':
                return
            
            self.auction.status = 'completed'
            if not self.auction.end_time or timezone.now() < self.auction.end_time:
                self.auction.end_time = timezone.now()
            
            # Determine winner (last human bidder)
            last_human_bid = self.auction.bids.filter(bidder_type='human').first()
            if last_human_bid:
                self.auction.winner = last_human_bid.bidder
            
            self.auction.save()
            
            # Create log
            winner_name = self.auction.winner.username if self.auction.winner else "No winner"
            AuctionLog.objects.create(
                auction=self.auction,
                event_type='completed',
                message=f"Auction completed. Winner: {winner_name}, Final price: ₹{self.auction.current_price}"
            )
            
            logger.info(f"Auction completed: {self.auction.id}, Winner: {winner_name}")

