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
        
        # Check if bot has reached max bid or if next bid would exceed it
        if self.auction.bot_current_bid >= self.auction.max_bid:
            return False
        
        # Check if next bid would exceed max bid
        next_bid = self.get_next_bid_amount()
        if next_bid > self.auction.max_bid:
            return False
        
        # Check if auction has time remaining or can be extended
        if self.auction.remaining_time <= 0 and self.auction.current_phase != 3:
            return False
        
        return True
    
    def get_next_bid_amount(self):
        """Calculate the next bid amount."""
        current = float(self.auction.current_price)
        max_bid = float(self.auction.max_bid)
        
        # Choose a random increment
        increment = random.choice(self.bid_increments)
        next_bid = current + increment
        
        # Ensure we don't exceed max_bid
        if next_bid > max_bid:
            next_bid = max_bid
        
        # Ensure the bid is at least minimum increment above current price
        min_bid = current + min(self.bid_increments)
        if next_bid < min_bid:
            next_bid = min_bid
        
        return next_bid
    
    def should_bid_in_phase_1(self, elapsed_time, phase_duration):
        """Determine if bot should bid in Phase 1."""
        logger.info(f"Phase 1 check: elapsed={elapsed_time:.1f}s, duration={phase_duration:.1f}s")
        
        # Check if human has bid recently (within last 10 seconds)
        recent_human_bid = self.auction.bids.filter(
            bidder_type='human',
            timestamp__gte=timezone.now() - timezone.timedelta(seconds=10)
        ).exists()
        
        if recent_human_bid:
            logger.info("Human bid detected in Phase 1, bot will react")
            return True
        
        # Bid after 50% of Phase 1 (more aggressive than default 75%)
        wait_percentage = 0.5
        wait_time = phase_duration * wait_percentage
        
        if elapsed_time >= wait_time:
            # Check if bot has already bid in this phase
            phase_bids = self.auction.bids.filter(
                bidder_type='bot',
                phase=1
            ).exists()
            
            if not phase_bids:
                logger.info(f"Bot will bid in Phase 1 after waiting {wait_time:.1f}s")
                return True
        
        return False
    
    def should_bid_in_phase_2(self, elapsed_time, phase_start, phase_duration):
        """Determine if bot should bid in Phase 2."""
        phase_elapsed = elapsed_time - phase_start
        logger.info(f"Phase 2 check: phase_elapsed={phase_elapsed:.1f}s, duration={phase_duration:.1f}s")
        
        # Check if human has bid recently (within last 10 seconds - same as Phase 1)
        recent_human_bid = self.auction.bids.filter(
            bidder_type='human',
            timestamp__gte=timezone.now() - timezone.timedelta(seconds=10)
        ).exists()
        
        if recent_human_bid:
            logger.info("Human bid detected in Phase 2, bot will react")
            return True
        
        # More aggressive: Wait only 60% of Phase 2 (instead of 75%)
        wait_percentage = 0.6
        wait_time = phase_duration * wait_percentage
        
        # If no human bid, bid once after 60% of phase
        if phase_elapsed >= wait_time:
            phase_bids = self.auction.bids.filter(
                bidder_type='bot',
                phase=2
            ).exists()
            
            if not phase_bids:
                logger.info(f"Bot will bid in Phase 2 after waiting {wait_time:.1f}s")
                return True
        
        return False
    
    def should_bid_in_phase_3(self):
        """Determine if bot should bid in Phase 3."""
        # Check if human has bid recently (within last 10 seconds)
        recent_human_bid = self.auction.bids.filter(
            bidder_type='human',
            timestamp__gte=timezone.now() - timezone.timedelta(seconds=10)
        ).exists()
        
        if recent_human_bid:
            logger.info("Human bid detected in Phase 3, bot will react")
            return True
        
        # If no recent human bids, use probability (but higher chance)
        probability = min(0.60, self.config['PHASE_3_BID_PROBABILITY'] * 2)  # 60% chance
        should_bid = random.random() < probability
        
        if should_bid:
            logger.info("Bot decided to bid in Phase 3 (random)")
        
        return should_bid
    
    def get_reaction_delay(self):
        """Get random reaction delay for bot."""
        min_delay = self.config['BOT_REACTION_DELAY_MIN']
        max_delay = self.config['BOT_REACTION_DELAY_MAX']
        return random.uniform(min_delay, max_delay)
    
    def place_bid(self, phase=None):
        """Place a bid on behalf of the bot."""
        logger.info(f"Bot attempting to place bid for auction {self.auction.id}")
        
        if not self.can_bid():
            logger.info("Bot cannot bid - conditions not met")
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
            
            # Update auction - only update current_price if this bid is higher
            if next_bid > self.auction.current_price:
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
        
        # Check if max bid reached (by anyone)
        if self.auction.current_price >= self.auction.max_bid:
            self.complete_auction()
            return
        
        # Check if time expired
        if self.auction.remaining_time <= 0:
            # In Phase 3, allow some extension time for final bids, but eventually complete
            if self.auction.current_phase == 3:
                # Check if we've extended too much (more than 30 seconds past original end)
                if self.auction.extended_time > 30:
                    self.complete_auction()
                    return
            else:
                # Complete immediately if not in Phase 3
                self.complete_auction()
                return
    
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

