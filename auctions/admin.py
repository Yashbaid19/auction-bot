from django.contrib import admin
from .models import Auction, Bid, AuctionLog


@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    """Admin interface for Auction model."""
    list_display = ['title', 'status', 'current_price', 'max_bid', 
                    'current_phase', 'remaining_time', 'winner', 'created_by', 'created_at']
    list_filter = ['status', 'bot_active', 'created_at']
    search_fields = ['title', 'description', 'created_by__username']
    readonly_fields = ['id', 'current_price', 'start_time', 'end_time', 
                      'extended_time', 'bot_current_bid', 'winner', 
                      'created_at', 'updated_at', 'current_phase', 
                      'phase_progress', 'remaining_time', 'elapsed_time']
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'title', 'description', 'created_by')
        }),
        ('Pricing', {
            'fields': ('start_price', 'max_bid', 'current_price')
        }),
        ('Timing', {
            'fields': ('duration', 'start_time', 'end_time', 'extended_time',
                      'remaining_time', 'elapsed_time')
        }),
        ('Status', {
            'fields': ('status', 'current_phase', 'phase_progress', 'winner')
        }),
        ('Bot Configuration', {
            'fields': ('bot_active', 'bot_current_bid')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    """Admin interface for Bid model."""
    list_display = ['auction', 'bidder', 'bidder_type', 'amount', 'phase', 'timestamp']
    list_filter = ['bidder_type', 'phase', 'timestamp']
    search_fields = ['auction__title', 'bidder__username']
    readonly_fields = ['id', 'timestamp']


@admin.register(AuctionLog)
class AuctionLogAdmin(admin.ModelAdmin):
    """Admin interface for AuctionLog model."""
    list_display = ['auction', 'event_type', 'timestamp']
    list_filter = ['event_type', 'timestamp']
    search_fields = ['auction__title', 'message']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']

