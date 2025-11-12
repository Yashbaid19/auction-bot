from rest_framework import viewsets, status, generics
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q, Count, Sum, Avg
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.conf import settings
import logging

from .models import Auction, Bid, AuctionLog
from .serializers import (
    AuctionSerializer, AuctionDetailSerializer, BidSerializer,
    BidCreateSerializer, AuctionCreateSerializer, AuctionStatsSerializer
)
from .bot_logic import AuctionBot
from .bot_runner import start_auction_bot, stop_auction_bot

logger = logging.getLogger('auctions')

# Frontend Views
def home(request):
    """Home page with active auctions."""
    active_auctions = Auction.objects.filter(status='active').order_by('-start_time')
    pending_auctions = Auction.objects.filter(status='pending').order_by('-created_at')
    recent_auctions = Auction.objects.filter(status='completed').order_by('-end_time')[:5]
    return render(request, 'auctions/home.html', {
        'active_auctions': active_auctions,
        'pending_auctions': pending_auctions,
        'recent_auctions': recent_auctions
    })

def auction_detail(request, auction_id):
    """Auction detail page with real-time updates."""
    auction = get_object_or_404(Auction, id=auction_id)
    bids = auction.bids.all().order_by('-timestamp')[:20]
    logs = auction.logs.all().order_by('-timestamp')[:10]
    
    # Calculate bid counts
    human_bids_count = auction.bids.filter(bidder_type='human').count()
    bot_bids_count = auction.bids.filter(bidder_type='bot').count()
    
    return render(request, 'auctions/auction_detail.html', {
        'auction': auction,
        'bids': bids,
        'logs': logs,
        'human_bids_count': human_bids_count,
        'bot_bids_count': bot_bids_count,
    })

def create_auction(request):
    """Create new auction page."""
    if request.method == 'POST':
        # Handle form submission via API
        pass
    return render(request, 'auctions/create_auction.html')

def my_auctions_view(request):
    """User's auctions page."""
    if not request.user.is_authenticated:
        from django.shortcuts import redirect
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.get_full_path())
    
    my_auctions = Auction.objects.filter(created_by=request.user).order_by('-created_at')
    my_bids = Bid.objects.filter(bidder=request.user, bidder_type='human').order_by('-timestamp')
    return render(request, 'auctions/my_auctions.html', {
        'my_auctions': my_auctions,
        'my_bids': my_bids
    })

def statistics_view(request):
    """Statistics dashboard."""
    stats = {
        'total_auctions': Auction.objects.count(),
        'active_auctions': Auction.objects.filter(status='active').count(),
        'pending_auctions': Auction.objects.filter(status='pending').count(),
        'completed_auctions': Auction.objects.filter(status='completed').count(),
        'cancelled_auctions': Auction.objects.filter(status='cancelled').count(),
        'total_bids': Bid.objects.count(),
        'human_bids': Bid.objects.filter(bidder_type='human').count(),
        'bot_bids': Bid.objects.filter(bidder_type='bot').count(),
    }
    return render(request, 'auctions/statistics.html', {'stats': stats})

class AuctionViewSet(viewsets.ModelViewSet):
    """ViewSet for Auction CRUD operations."""
    queryset = Auction.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'created_by']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'start_time', 'current_price']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AuctionDetailSerializer
        elif self.action == 'create':
            return AuctionCreateSerializer
        return AuctionSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Allow filtering by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, current_price=serializer.validated_data['start_price'])
        logger.info(f"Auction created: {serializer.instance.title} by {self.request.user.username}")
    
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """Start an auction."""
        auction = self.get_object()
        
        if auction.status != 'pending':
            return Response(
                {'error': 'Auction can only be started if it is pending.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if auction.created_by != request.user:
            return Response(
                {'error': 'Only the creator can start the auction.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Start the auction
        auction.status = 'active'
        auction.start_time = timezone.now()
        auction.end_time = auction.start_time + timezone.timedelta(seconds=auction.duration)
        auction.current_price = auction.start_price
        auction.save()
        
        # Create initial log
        AuctionLog.objects.create(
            auction=auction,
            event_type='started',
            message=f"Auction started. Duration: {auction.duration}s, Max bid: ₹{auction.max_bid}"
        )
        
        # Start bot if enabled
        if auction.bot_active:
            start_auction_bot(str(auction.id))
            logger.info(f"Bot started for auction: {auction.id}")
        
        # No WebSocket broadcast needed (simplified version)
        
        serializer = self.get_serializer(auction)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def bot_status(self, request, pk=None):
        """Check if bot is running for this auction."""
        auction = self.get_object()
        
        from .bot_runner import _running_bots
        import threading
        
        auction_id_str = str(auction.id)
        is_running = auction_id_str in _running_bots
        thread_alive = False
        
        if is_running:
            thread = _running_bots[auction_id_str]
            thread_alive = thread.is_alive()
        
        return Response({
            'auction_id': auction_id_str,
            'bot_active': auction.bot_active,
            'bot_thread_exists': is_running,
            'bot_thread_alive': thread_alive,
            'active_threads': len(_running_bots),
            'all_threads': [t.name for t in threading.enumerate() if 'AuctionBot' in t.name]
        })
    
    @action(detail=True, methods=['post'])
    def stop(self, request, pk=None):
        """Stop an auction manually."""
        auction = self.get_object()
        
        if auction.status != 'active':
            return Response(
                {'error': 'Auction is not active.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if auction.created_by != request.user:
            return Response(
                {'error': 'Only the creator can stop the auction.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Stop the auction
        stop_auction_bot(str(auction.id))
        auction.status = 'completed'
        auction.end_time = timezone.now()
        
        # Determine winner (last human bidder)
        last_human_bid = auction.bids.filter(bidder_type='human').first()
        if last_human_bid:
            auction.winner = last_human_bid.bidder
        
        auction.save()
        
        AuctionLog.objects.create(
            auction=auction,
            event_type='completed',
            message=f"Auction stopped manually by {request.user.username}"
        )
        
        # No WebSocket broadcast needed (simplified version)
        
        serializer = self.get_serializer(auction)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def bids(self, request, pk=None):
        """Get all bids for an auction."""
        auction = self.get_object()
        bids = auction.bids.all()
        serializer = BidSerializer(bids, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def logs(self, request, pk=None):
        """Get all logs for an auction."""
        auction = self.get_object()
        logs = auction.logs.all()
        from .serializers import AuctionLogSerializer
        serializer = AuctionLogSerializer(logs, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def status_info(self, request, pk=None):
        """Get detailed status information for an auction."""
        auction = self.get_object()
        
        data = {
            'status': auction.status,
            'current_phase': auction.current_phase,
            'phase_progress': auction.phase_progress,
            'remaining_time': auction.remaining_time,
            'elapsed_time': auction.elapsed_time,
            'current_price': float(auction.current_price),
            'max_bid': float(auction.max_bid),
            'bot_active': auction.bot_active,
            'bot_current_bid': float(auction.bot_current_bid),
            'total_bids': auction.bids.count(),
            'human_bids': auction.bids.filter(bidder_type='human').count(),
            'bot_bids': auction.bids.filter(bidder_type='bot').count(),
        }
        
        return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_bid(request, auction_id):
    """Place a bid on an auction."""
    auction = get_object_or_404(Auction, id=auction_id)
    
    serializer = BidCreateSerializer(data=request.data, context={'auction': auction})
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    amount = serializer.validated_data['amount']
    increment = serializer.validated_data.get('increment')
    
    # Calculate increment if not provided
    if not increment:
        difference = amount - auction.current_price
        valid_increments = settings.AUCTION_CONFIG['BID_INCREMENTS']
        # Find the closest valid increment
        increment = min(valid_increments, key=lambda x: abs(x - difference))
    
    # Create the bid
    bid = Bid.objects.create(
        auction=auction,
        bidder=request.user,
        bidder_type='human',
        amount=amount,
        phase=auction.current_phase
    )
    
    # Update auction
    auction.current_price = amount
    auction.save()
    
    # Create log
    AuctionLog.objects.create(
        auction=auction,
        event_type='bid_placed',
        message=f"Human bid placed: ₹{amount} by {request.user.username}",
        metadata={'bidder': request.user.username, 'amount': float(amount), 'phase': auction.current_phase}
    )
    
    logger.info(f"Bid placed: ₹{amount} by {request.user.username} on auction {auction.id}")
    
    # No WebSocket broadcast needed (simplified version)
    
    return Response(BidSerializer(bid).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([AllowAny])
def active_auctions(request):
    """Get all active auctions."""
    auctions = Auction.objects.filter(status='active')
    serializer = AuctionSerializer(auctions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_auctions(request):
    """Get auctions created by the current user."""
    auctions = Auction.objects.filter(created_by=request.user)
    serializer = AuctionSerializer(auctions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_bids(request):
    """Get all bids placed by the current user."""
    bids = Bid.objects.filter(bidder=request.user, bidder_type='human')
    serializer = BidSerializer(bids, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def statistics(request):
    """Get auction statistics."""
    total_auctions = Auction.objects.count()
    active_auctions = Auction.objects.filter(status='active').count()
    completed_auctions = Auction.objects.filter(status='completed').count()
    
    total_bids = Bid.objects.count()
    total_revenue = Auction.objects.filter(status='completed', winner__isnull=False).aggregate(
        total=Sum('current_price')
    )['total'] or 0
    
    avg_bid = Bid.objects.aggregate(avg=Avg('amount'))['avg'] or 0
    
    # Top bidders
    top_bidders = Bid.objects.filter(bidder_type='human').values('bidder__username').annotate(
        bid_count=Count('id'),
        total_amount=Sum('amount')
    ).order_by('-bid_count')[:10]
    
    recent_auctions = Auction.objects.filter(status='completed').order_by('-end_time')[:5]
    
    data = {
        'total_auctions': total_auctions,
        'active_auctions': active_auctions,
        'completed_auctions': completed_auctions,
        'total_bids': total_bids,
        'total_revenue': float(total_revenue),
        'average_bid_amount': float(avg_bid),
        'top_bidders': list(top_bidders),
        'recent_auctions': AuctionSerializer(recent_auctions, many=True).data
    }
    
    serializer = AuctionStatsSerializer(data)
    return Response(serializer.data)
