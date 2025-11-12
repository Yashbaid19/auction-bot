from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid

User = get_user_model()


class Auction(models.Model):
    """Auction model with phase-based timing."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_price = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)
    max_bid = models.DecimalField(max_digits=10, decimal_places=2, help_text="Bot's maximum bid limit")
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    duration = models.IntegerField(default=90, help_text="Total duration in seconds")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Timing fields
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    extended_time = models.IntegerField(default=0, help_text="Total extended time in seconds")
    
    # Bot configuration
    bot_active = models.BooleanField(default=True)
    bot_current_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Winner
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_auctions')
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_auctions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'auctions'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.status}"
    
    @property
    def elapsed_time(self):
        """Calculate elapsed time in seconds."""
        if not self.start_time:
            return 0
        now = timezone.now()
        if self.end_time and now > self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return (now - self.start_time).total_seconds()
    
    @property
    def remaining_time(self):
        """Calculate remaining time in seconds."""
        if self.status == 'pending':
            return self.duration  # Show full duration for pending auctions
        if not self.start_time or not self.end_time:
            return 0
        now = timezone.now()
        remaining = (self.end_time - now).total_seconds()
        return max(0, remaining)
    
    @property
    def current_phase(self):
        """Determine current phase (1, 2, or 3)."""
        if not self.start_time or self.status != 'active':
            return None
        
        elapsed = self.elapsed_time
        total_duration = self.duration
        
        phase_1_end = total_duration * 0.25
        phase_2_end = total_duration * 0.75
        
        if elapsed <= phase_1_end:
            return 1
        elif elapsed <= phase_2_end:
            return 2
        else:
            return 3
    
    @property
    def phase_progress(self):
        """Calculate progress within current phase (0-1)."""
        if not self.start_time or self.status != 'active':
            return 0
        
        elapsed = self.elapsed_time
        total_duration = self.duration
        
        phase_1_end = total_duration * 0.25
        phase_2_end = total_duration * 0.75
        
        if elapsed <= phase_1_end:
            return elapsed / phase_1_end
        elif elapsed <= phase_2_end:
            return (elapsed - phase_1_end) / (phase_2_end - phase_1_end)
        else:
            return min(1.0, (elapsed - phase_2_end) / (total_duration - phase_2_end))


class Bid(models.Model):
    """Bid model for tracking all bids."""
    BIDDER_TYPE_CHOICES = [
        ('human', 'Human'),
        ('bot', 'Bot'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='bids')
    bidder_type = models.CharField(max_length=10, choices=BIDDER_TYPE_CHOICES, default='human')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phase = models.IntegerField(null=True, blank=True, help_text="Phase when bid was placed")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'bids'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['auction', '-timestamp']),
        ]
    
    def __str__(self):
        bidder_name = self.bidder.username if self.bidder else 'Bot'
        return f"{bidder_name} - ₹{self.amount} - {self.auction.title}"


class AuctionLog(models.Model):
    """Log model for tracking auction events."""
    EVENT_TYPE_CHOICES = [
        ('started', 'Auction Started'),
        ('bid_placed', 'Bid Placed'),
        ('phase_changed', 'Phase Changed'),
        ('extended', 'Time Extended'),
        ('completed', 'Auction Completed'),
        ('bot_action', 'Bot Action'),
    ]
    
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='logs')
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    message = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'auction_logs'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.event_type} - {self.auction.title} - {self.timestamp}"

