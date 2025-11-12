from django.core.management.base import BaseCommand
from auctions.models import Auction
from auctions.bot_runner import start_auction_bot
import logging

logger = logging.getLogger('auctions')

class Command(BaseCommand):
    help = 'Restart bots for all active auctions'

    def handle(self, *args, **options):
        active_auctions = Auction.objects.filter(status='active', bot_active=True)
        
        self.stdout.write(f'Found {active_auctions.count()} active auctions with bots enabled')
        
        for auction in active_auctions:
            try:
                start_auction_bot(str(auction.id))
                self.stdout.write(
                    self.style.SUCCESS(f'Started bot for auction: {auction.title} ({auction.id})')
                )
                logger.info(f'Bot restarted for auction {auction.id}')
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Failed to start bot for auction {auction.id}: {str(e)}')
                )
                logger.error(f'Failed to restart bot for auction {auction.id}: {str(e)}')
        
        self.stdout.write(self.style.SUCCESS('Bot restart completed'))
