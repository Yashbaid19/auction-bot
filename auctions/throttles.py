"""
Custom throttling classes for auction endpoints.
"""
from rest_framework.throttling import UserRateThrottle


class BiddingRateThrottle(UserRateThrottle):
    """Custom throttle for bidding endpoints."""
    scope = 'bidding'

