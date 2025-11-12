from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.AuctionViewSet, basename='auction')

urlpatterns = [
    # API endpoints (for REST API)
    path('', include(router.urls)),
    path('<uuid:auction_id>/bid/', views.place_bid, name='place-bid'),
    path('<uuid:auction_id>/start/', views.AuctionViewSet.as_view({'post': 'start'}), name='auction-start'),
    path('<uuid:auction_id>/stop/', views.AuctionViewSet.as_view({'post': 'stop'}), name='auction-stop'),
    path('<uuid:auction_id>/delete_pending/', views.AuctionViewSet.as_view({'delete': 'delete_pending'}), name='auction-delete'),
    path('<uuid:auction_id>/bids/', views.AuctionViewSet.as_view({'get': 'bids'}), name='auction-bids'),
    path('<uuid:auction_id>/logs/', views.AuctionViewSet.as_view({'get': 'logs'}), name='auction-logs'),
    path('<uuid:auction_id>/status_info/', views.AuctionViewSet.as_view({'get': 'status_info'}), name='auction-status'),
    path('active/', views.active_auctions, name='active-auctions'),
    path('my-auctions/', views.my_auctions, name='my-auctions'),
    path('my-bids/', views.my_bids, name='my-bids'),
    path('statistics/', views.statistics, name='statistics'),
]

