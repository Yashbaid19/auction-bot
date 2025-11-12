from django.urls import path
from . import views

app_name = 'auctions'

urlpatterns = [
    # Frontend views (HTML pages) - at root level
    path('', views.home, name='home'),
    path('create/', views.create_auction, name='create-auction'),
    path('my-auctions/', views.my_auctions_view, name='my-auctions-view'),
    path('completed/', views.completed_auctions_view, name='completed-auctions'),
    path('completed/<uuid:auction_id>/', views.completed_auction_detail_view, name='completed-auction-detail'),
    path('statistics/', views.statistics_view, name='statistics-view'),
    path('<uuid:auction_id>/', views.auction_detail, name='auction-detail'),
]

