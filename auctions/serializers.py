from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Auction, Bid, AuctionLog
from django.conf import settings

User = get_user_model()


class BidSerializer(serializers.ModelSerializer):
    """Serializer for Bid model."""
    bidder_username = serializers.CharField(source='bidder.username', read_only=True)
    bidder_type_display = serializers.CharField(source='get_bidder_type_display', read_only=True)
    
    class Meta:
        model = Bid
        fields = ['id', 'auction', 'bidder', 'bidder_username', 'bidder_type', 
                  'bidder_type_display', 'amount', 'phase', 'timestamp']
        read_only_fields = ['id', 'timestamp', 'phase']


class AuctionLogSerializer(serializers.ModelSerializer):
    """Serializer for AuctionLog model."""
    event_type_display = serializers.CharField(source='get_event_type_display', read_only=True)
    
    class Meta:
        model = AuctionLog
        fields = ['id', 'auction', 'event_type', 'event_type_display', 
                  'message', 'metadata', 'timestamp']
        read_only_fields = ['id', 'timestamp']


class AuctionSerializer(serializers.ModelSerializer):
    """Serializer for Auction model."""
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    winner_username = serializers.CharField(source='winner.username', read_only=True)
    current_phase = serializers.IntegerField(read_only=True)
    phase_progress = serializers.FloatField(read_only=True)
    remaining_time = serializers.FloatField(read_only=True)
    elapsed_time = serializers.FloatField(read_only=True)
    total_bids = serializers.SerializerMethodField()
    human_bids_count = serializers.SerializerMethodField()
    bot_bids_count = serializers.SerializerMethodField()
    latest_bid = serializers.SerializerMethodField()
    
    class Meta:
        model = Auction
        fields = ['id', 'title', 'description', 'start_price', 'max_bid', 
                  'current_price', 'duration', 'status', 'start_time', 'end_time',
                  'extended_time', 'bot_active', 'bot_current_bid', 'winner',
                  'winner_username', 'created_by', 'created_by_username',
                  'created_at', 'updated_at', 'current_phase', 'phase_progress',
                  'remaining_time', 'elapsed_time', 'total_bids', 
                  'human_bids_count', 'bot_bids_count', 'latest_bid']
        read_only_fields = ['id', 'current_price', 'status', 'start_time', 
                           'end_time', 'extended_time', 'bot_current_bid',
                           'winner', 'created_at', 'updated_at']
    
    def get_total_bids(self, obj):
        return obj.bids.count()
    
    def get_human_bids_count(self, obj):
        return obj.bids.filter(bidder_type='human').count()
    
    def get_bot_bids_count(self, obj):
        return obj.bids.filter(bidder_type='bot').count()
    
    def get_latest_bid(self, obj):
        latest = obj.bids.first()
        if latest:
            return BidSerializer(latest).data
        return None


class AuctionDetailSerializer(AuctionSerializer):
    """Detailed serializer with bids and logs."""
    bids = BidSerializer(many=True, read_only=True)
    logs = AuctionLogSerializer(many=True, read_only=True)
    
    class Meta(AuctionSerializer.Meta):
        fields = AuctionSerializer.Meta.fields + ['bids', 'logs']


class BidCreateSerializer(serializers.Serializer):
    """Serializer for creating a bid."""
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    increment = serializers.ChoiceField(
        choices=[100, 500, 1000],
        required=False,
        help_text="Bid increment (100, 500, or 1000). If not provided, will be calculated automatically."
    )
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Bid amount must be positive.")
        return value
    
    def validate(self, attrs):
        auction = self.context['auction']
        amount = attrs['amount']
        increment = attrs.get('increment')
        
        # Check if auction is active
        if auction.status != 'active':
            raise serializers.ValidationError("Auction is not active.")
        
        # Check if auction has ended
        if auction.remaining_time <= 0:
            raise serializers.ValidationError("Auction has ended.")
        
        # Validate bid increment
        valid_increments = settings.AUCTION_CONFIG['BID_INCREMENTS']
        if increment and increment not in valid_increments:
            raise serializers.ValidationError(
                f"Increment must be one of: {valid_increments}"
            )
        
        # Calculate minimum bid
        min_bid = auction.current_price + min(valid_increments)
        if amount < min_bid:
            raise serializers.ValidationError(
                f"Bid must be at least ₹{min_bid}. Current price is ₹{auction.current_price}."
            )
        
        # Check if increment matches
        if increment:
            difference = amount - auction.current_price
            if difference not in valid_increments:
                raise serializers.ValidationError(
                    f"Bid increment must be one of: {valid_increments}"
                )
        
        return attrs


class AuctionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating an auction."""
    
    class Meta:
        model = Auction
        fields = ['title', 'description', 'start_price', 'max_bid', 
                  'duration', 'bot_active']
    
    def validate_max_bid(self, value):
        if value <= 0:
            raise serializers.ValidationError("Max bid must be positive.")
        return value
    
    def validate_start_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Start price must be positive.")
        return value
    
    def validate(self, attrs):
        start_price = attrs.get('start_price', 0)
        max_bid = attrs.get('max_bid', 0)
        
        if max_bid <= start_price:
            raise serializers.ValidationError(
                "Max bid must be greater than start price."
            )
        
        return attrs


class AuctionStatsSerializer(serializers.Serializer):
    """Serializer for auction statistics."""
    total_auctions = serializers.IntegerField()
    active_auctions = serializers.IntegerField()
    completed_auctions = serializers.IntegerField()
    total_bids = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    average_bid_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    top_bidders = serializers.ListField()
    recent_auctions = AuctionSerializer(many=True)

