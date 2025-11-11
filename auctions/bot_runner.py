"""
Simple bot runner using threading (no Celery/Redis needed).
"""
import threading
import time
import logging
from django.utils import timezone
from .models import Auction
from .bot_logic import AuctionBot

logger = logging.getLogger('auctions')

# Store running bot threads
_running_bots = {}


def start_auction_bot(auction_id):
    """Start bot for an auction using threading."""
    auction_id_str = str(auction_id)
    
    # Stop existing bot if running
    if auction_id_str in _running_bots:
        stop_auction_bot(auction_id_str)
    
    # Start new bot thread
    thread = threading.Thread(
        target=_run_bot,
        args=(auction_id_str,),
        daemon=True
    )
    thread.start()
    _running_bots[auction_id_str] = thread
    logger.info(f"Bot thread started for auction {auction_id_str}")


def stop_auction_bot(auction_id):
    """Stop bot for an auction."""
    auction_id_str = str(auction_id)
    if auction_id_str in _running_bots:
        # Mark as stopped (thread will check and exit)
        _running_bots.pop(auction_id_str, None)
        logger.info(f"Bot thread stopped for auction {auction_id_str}")


def _run_bot(auction_id_str):
    """Main bot loop running in thread."""
    while auction_id_str in _running_bots:
        try:
            auction = Auction.objects.get(id=auction_id_str)
            
            if auction.status != 'active':
                break
            
            if not auction.bot_active:
                break
            
            bot = AuctionBot(auction)
            
            # Check if auction should be completed
            bot.check_and_complete()
            
            # Refresh auction
            auction.refresh_from_db()
            if auction.status != 'active':
                break
            
            # Get phase information
            phase = auction.current_phase
            if phase is None:
                time.sleep(2)
                continue
            
            elapsed_time = auction.elapsed_time
            total_duration = auction.duration
            phase_1_end = total_duration * 0.25
            phase_2_end = total_duration * 0.75
            
            # Process based on phase
            if phase == 1:
                result = bot.process_phase_1(elapsed_time, phase_1_end)
                if result == 'react':
                    # Schedule delayed reaction
                    time.sleep(bot.get_reaction_delay())
                    bot.place_bid(phase=1)
            elif phase == 2:
                phase_2_duration = phase_2_end - phase_1_end
                result = bot.process_phase_2(elapsed_time, phase_1_end, phase_2_duration)
                if result == 'react':
                    time.sleep(bot.get_reaction_delay())
                    bot.place_bid(phase=2)
            elif phase == 3:
                bot.process_phase_3()
            
            # Sleep before next check
            if phase == 3:
                time.sleep(1)  # Check every second in Phase 3
            else:
                time.sleep(2)  # Check every 2 seconds in other phases
        
        except Auction.DoesNotExist:
            logger.error(f"Auction {auction_id_str} not found")
            break
        except Exception as e:
            logger.error(f"Error in bot for {auction_id_str}: {str(e)}")
            time.sleep(5)  # Wait before retrying
    
    # Clean up
    _running_bots.pop(auction_id_str, None)
    logger.info(f"Bot thread ended for auction {auction_id_str}")

