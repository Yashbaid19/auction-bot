from django.core.management.base import BaseCommand
from auctions.models import Auction


class Command(BaseCommand):
    help = 'Fix auction winners for completed auctions where bot should be the winner'

    def handle(self, *args, **options):
        # Get all completed auctions
        completed_auctions = Auction.objects.filter(status='completed')
        
        fixed_count = 0
        
        for auction in completed_auctions:
            # Get the last bid (highest bid)
            last_bid = auction.bids.first()  # Already ordered by -timestamp
            
            if last_bid:
                # Check if the current winner is correct
                if last_bid.bidder_type == 'bot':
                    # Bot should be the winner, but winner field should be None
                    if auction.winner is not None:
                        self.stdout.write(
                            f"Fixing auction {auction.title} (ID: {auction.id}): "
                            f"Bot won with ₹{last_bid.amount}, but winner was set to {auction.winner.username}"
                        )
                        auction.winner = None
                        auction.save()
                        fixed_count += 1
                elif last_bid.bidder_type == 'human':
                    # Human should be the winner
                    if auction.winner != last_bid.bidder:
                        self.stdout.write(
                            f"Fixing auction {auction.title} (ID: {auction.id}): "
                            f"Human {last_bid.bidder.username} won with ₹{last_bid.amount}"
                        )
                        auction.winner = last_bid.bidder
                        auction.save()
                        fixed_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully fixed {fixed_count} auction winners')
        )
