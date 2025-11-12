from django.apps import AppConfig
import os


class AuctionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auctions'
    
    def ready(self):
        import auctions.signals  # noqa
        
        # Auto-start bots for active auctions on server startup
        # Only run this in production or when explicitly needed
        # Skip during development server reloads and shell commands
        if self._should_auto_start_bots():
            self._start_existing_bots()
    
    def _start_existing_bots(self):
        """Start bots for all active auctions on server startup."""
        try:
            # Import here to avoid circular imports
            from .models import Auction
            from .bot_runner import start_auction_bot
            import logging
            
            logger = logging.getLogger('auctions')
            
            # Find all active auctions with bots enabled
            active_auctions = Auction.objects.filter(
                status='active',
                bot_active=True
            )
            
            logger.info(f"Starting bots for {active_auctions.count()} active auctions on server startup")
            
            for auction in active_auctions:
                try:
                    start_auction_bot(str(auction.id))
                    logger.info(f"Auto-started bot for auction: {auction.title} ({auction.id})")
                except Exception as e:
                    logger.error(f"Failed to start bot for auction {auction.id}: {e}")
                    
        except Exception as e:
            # Don't crash Django startup if bot starting fails
            import logging
            logger = logging.getLogger('auctions')
            logger.error(f"Failed to auto-start bots on startup: {e}")
    
    def _should_auto_start_bots(self):
        """Determine if we should auto-start bots."""
        import sys
        
        # Skip if running shell commands
        if 'shell' in sys.argv:
            return False
            
        # Skip if running migrations or other management commands
        if len(sys.argv) > 1 and sys.argv[1] in ['migrate', 'makemigrations', 'collectstatic', 'shell', 'test']:
            return False
            
        # Skip if in development and this is a reload (RUN_MAIN is set by Django dev server)
        if os.environ.get('RUN_MAIN') == 'true':
            return False
            
        # Auto-start in production or first development server start
        return True

