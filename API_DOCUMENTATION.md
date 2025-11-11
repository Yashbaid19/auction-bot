# 📚 Complete API Documentation

Complete, detailed API reference for the Auction Bot system with step-by-step examples.

## 📋 Table of Contents

1. [Base URL and Setup](#base-url-and-setup)
2. [Authentication](#authentication)
3. [Authentication Endpoints](#authentication-endpoints)
4. [Auction Endpoints](#auction-endpoints)
5. [Bidding Endpoints](#bidding-endpoints)
6. [Statistics Endpoint](#statistics-endpoint)
7. [Error Handling](#error-handling)
8. [Rate Limiting](#rate-limiting)
9. [Example Workflows](#example-workflows)

---

## Base URL and Setup

### Local Development
```
http://localhost:8000/api
```

### Production (After Deployment)
```
https://your-app-name.onrender.com/api
```

### Interactive Documentation

**Swagger UI** (Recommended for testing):
- Local: http://localhost:8000/swagger/
- Production: https://your-app.onrender.com/swagger/

**ReDoc** (Alternative documentation):
- Local: http://localhost:8000/redoc/
- Production: https://your-app.onrender.com/redoc/

**How to Use Swagger**:
1. Open the Swagger URL in your browser
2. You'll see all available endpoints
3. Click on any endpoint to expand it
4. Click "Try it out" to test
5. Fill in the parameters
6. Click "Execute" to send the request
7. See the response below

---

## Authentication

### Overview

Most API endpoints require authentication. You need to include a token in your requests.

### How Authentication Works

1. **Register or Login** to get a token
2. **Include the token** in all subsequent requests
3. **Token format**: `Token <your-token-here>`

### Getting Your Token

**Method 1: Register a New User**

See [Register User](#register-user) endpoint below.

**Method 2: Login**

See [Login](#login) endpoint below.

**Both methods return a token** in the response. Save this token!

### Using Your Token

**In HTTP Headers**:
```
Authorization: Token abc123def456ghi789...
```

**In Swagger UI**:
1. Click the **"Authorize"** button (top right, lock icon)
2. In the popup, enter: `Token YOUR_TOKEN_HERE`
3. Click "Authorize"
4. Now all requests will include your token automatically

**In Code (Python)**:
```python
import requests

headers = {
    'Authorization': 'Token YOUR_TOKEN_HERE',
    'Content-Type': 'application/json'
}

response = requests.get('http://localhost:8000/api/auctions/', headers=headers)
```

**In Code (JavaScript)**:
```javascript
fetch('http://localhost:8000/api/auctions/', {
    headers: {
        'Authorization': 'Token YOUR_TOKEN_HERE',
        'Content-Type': 'application/json'
    }
})
```

---

## Authentication Endpoints

### Register User

**What this does**: Creates a new user account and returns an authentication token.

**Endpoint**: `POST /api/auth/api/register/`

**Authentication Required**: No

**Request Body**:
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123",
  "password_confirm": "securepassword123",
  "phone_number": "+1234567890"
}
```

**Field Details**:
- `username` (required): Unique username, 150 characters max
- `email` (required): Valid email address, must be unique
- `password` (required): Minimum 8 characters
- `password_confirm` (required): Must match password exactly
- `phone_number` (optional): Phone number in any format

**Example Request (cURL)**:
```bash
curl -X POST http://localhost:8000/api/auth/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "phone_number": "+1234567890"
  }'
```

**Example Request (PowerShell)**:
```powershell
$body = @{
    username = "john_doe"
    email = "john@example.com"
    password = "securepassword123"
    password_confirm = "securepassword123"
    phone_number = "+1234567890"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/auth/api/register/" `
  -Method POST `
  -Body $body `
  -ContentType "application/json"
```

**Success Response** (201 Created):
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "phone_number": "+1234567890",
    "date_joined": "2024-01-15T10:30:00Z",
    "created_at": "2024-01-15T10:30:00Z"
  },
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "message": "User registered successfully."
}
```

**Error Response** (400 Bad Request):
```json
{
  "username": ["A user with that username already exists."],
  "email": ["user with this email already exists."],
  "password_confirm": ["Passwords don't match."]
}
```

**Common Errors**:
- `username already exists` - Choose a different username
- `email already exists` - Use a different email
- `passwords don't match` - Make sure password and password_confirm are identical
- `password too short` - Use at least 8 characters

---

### Login

**What this does**: Authenticates an existing user and returns a token.

**Endpoint**: `POST /api/auth/api/login/`

**Authentication Required**: No

**Request Body**:
```json
{
  "username": "john_doe",
  "password": "securepassword123"
}
```

**Field Details**:
- `username` (required): Your registered username
- `password` (required): Your password

**Example Request (cURL)**:
```bash
curl -X POST http://localhost:8000/api/auth/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepassword123"
  }'
```

**Success Response** (200 OK):
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "phone_number": "+1234567890",
    "date_joined": "2024-01-15T10:30:00Z",
    "created_at": "2024-01-15T10:30:00Z"
  },
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "message": "Login successful."
}
```

**Error Response** (400 Bad Request):
```json
{
  "non_field_errors": ["Invalid credentials."]
}
```

**Common Errors**:
- `Invalid credentials` - Wrong username or password
- `User account is disabled` - Account has been deactivated

---

### Get Profile

**What this does**: Returns information about the currently authenticated user.

**Endpoint**: `GET /api/auth/api/profile/`

**Authentication Required**: Yes (Token)

**Request Headers**:
```
Authorization: Token YOUR_TOKEN_HERE
```

**Example Request (cURL)**:
```bash
curl -X GET http://localhost:8000/api/auth/api/profile/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

**Success Response** (200 OK):
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "phone_number": "+1234567890",
  "date_joined": "2024-01-15T10:30:00Z",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### Logout

**What this does**: Invalidates your authentication token.

**Endpoint**: `POST /api/auth/api/logout/`

**Authentication Required**: Yes (Token)

**Request Headers**:
```
Authorization: Token YOUR_TOKEN_HERE
```

**Example Request (cURL)**:
```bash
curl -X POST http://localhost:8000/api/auth/api/logout/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

**Success Response** (200 OK):
```json
{
  "message": "Logout successful."
}
```

**Note**: After logout, you'll need to login again to get a new token.

---

## Auction Endpoints

### List All Auctions

**What this does**: Returns a paginated list of all auctions.

**Endpoint**: `GET /api/auctions/api/`

**Authentication Required**: Yes (Token)

**Query Parameters** (all optional):
- `status`: Filter by status (`pending`, `active`, `completed`, `cancelled`)
- `search`: Search in title and description
- `ordering`: Order by field (`created_at`, `start_time`, `current_price`, `-created_at`, etc.)
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)

**Example Requests**:

**Get all auctions**:
```bash
curl -X GET http://localhost:8000/api/auctions/api/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

**Get only active auctions**:
```bash
curl -X GET "http://localhost:8000/api/auctions/api/?status=active" \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

**Search for auctions**:
```bash
curl -X GET "http://localhost:8000/api/auctions/api/?search=watch" \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

**Sort by price (highest first)**:
```bash
curl -X GET "http://localhost:8000/api/auctions/api/?ordering=-current_price" \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

**Success Response** (200 OK):
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/auctions/api/?page=2",
  "previous": null,
  "results": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Vintage Watch",
      "description": "Rare vintage watch from 1950s",
      "start_price": "1000.00",
      "max_bid": "10000.00",
      "current_price": "1500.00",
      "duration": 90,
      "status": "active",
      "current_phase": 2,
      "phase_progress": 0.5,
      "remaining_time": 45.5,
      "elapsed_time": 44.5,
      "total_bids": 5,
      "human_bids_count": 3,
      "bot_bids_count": 2,
      "winner_username": null,
      "created_by_username": "john_doe",
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

**Response Fields Explained**:
- `count`: Total number of auctions
- `next`: URL for next page (null if last page)
- `previous`: URL for previous page (null if first page)
- `results`: Array of auction objects
- `current_phase`: 1, 2, or 3 (null if not active)
- `phase_progress`: 0.0 to 1.0 (progress within current phase)
- `remaining_time`: Seconds remaining (0 if ended)
- `elapsed_time`: Seconds elapsed since start

---

### Get Auction Details

**What this does**: Returns detailed information about a specific auction, including all bids and logs.

**Endpoint**: `GET /api/auctions/api/{auction_id}/`

**Authentication Required**: Yes (Token)

**URL Parameters**:
- `auction_id`: UUID of the auction

**Example Request**:
```bash
curl -X GET http://localhost:8000/api/auctions/api/550e8400-e29b-41d4-a716-446655440000/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

**Success Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Vintage Watch",
  "description": "Rare vintage watch from 1950s",
  "start_price": "1000.00",
  "max_bid": "10000.00",
  "current_price": "1500.00",
  "duration": 90,
  "status": "active",
  "current_phase": 2,
  "phase_progress": 0.5,
  "remaining_time": 45.5,
  "elapsed_time": 44.5,
  "total_bids": 5,
  "human_bids_count": 3,
  "bot_bids_count": 2,
  "winner_username": null,
  "created_by_username": "john_doe",
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "bids": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "auction": "550e8400-e29b-41d4-a716-446655440000",
      "bidder": 1,
      "bidder_username": "john_doe",
      "bidder_type": "human",
      "bidder_type_display": "Human",
      "amount": "1500.00",
      "phase": 2,
      "timestamp": "2024-01-15T10:30:00Z"
    }
  ],
  "logs": [
    {
      "id": "770e8400-e29b-41d4-a716-446655440002",
      "auction": "550e8400-e29b-41d4-a716-446655440000",
      "event_type": "started",
      "event_type_display": "Auction Started",
      "message": "Auction started. Duration: 90s, Max bid: ₹10000",
      "metadata": {},
      "timestamp": "2024-01-15T10:00:00Z"
    }
  ]
}
```

**Error Response** (404 Not Found):
```json
{
  "detail": "Not found."
}
```

---

### Create Auction

**What this does**: Creates a new auction (status will be "pending").

**Endpoint**: `POST /api/auctions/api/`

**Authentication Required**: Yes (Token)

**Request Body**:
```json
{
  "title": "Vintage Watch",
  "description": "Rare vintage watch from 1950s",
  "start_price": 1000,
  "max_bid": 10000,
  "duration": 90,
  "bot_active": true
}
```

**Field Details**:
- `title` (required): Auction title, max 200 characters
- `description` (optional): Detailed description
- `start_price` (required): Starting bid amount, must be > 0
- `max_bid` (required): Bot's maximum bid, must be > start_price
- `duration` (required): Auction duration in seconds, minimum 30
- `bot_active` (optional): Enable bot bidding (default: true)

**Example Request**:
```bash
curl -X POST http://localhost:8000/api/auctions/api/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Vintage Watch",
    "description": "Rare vintage watch from 1950s",
    "start_price": 1000,
    "max_bid": 10000,
    "duration": 90,
    "bot_active": true
  }'
```

**Success Response** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Vintage Watch",
  "description": "Rare vintage watch from 1950s",
  "start_price": "1000.00",
  "max_bid": "10000.00",
  "current_price": "1000.00",
  "duration": 90,
  "status": "pending",
  "bot_active": true,
  "created_by_username": "john_doe",
  "created_at": "2024-01-15T10:00:00Z"
}
```

**Error Response** (400 Bad Request):
```json
{
  "max_bid": ["Max bid must be greater than start price."],
  "start_price": ["Start price must be positive."]
}
```

---

### Start Auction

**What this does**: Starts a pending auction (changes status to "active" and begins bot if enabled).

**Endpoint**: `POST /api/auctions/api/{auction_id}/start/`

**Authentication Required**: Yes (Token)

**Who Can Start**: Only the user who created the auction

**Example Request**:
```bash
curl -X POST http://localhost:8000/api/auctions/api/550e8400-e29b-41d4-a716-446655440000/start/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

**Success Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "active",
  "start_time": "2024-01-15T10:30:00Z",
  "end_time": "2024-01-15T10:31:30Z",
  "current_phase": 1,
  "remaining_time": 90.0,
  ...
}
```

**Error Responses**:

**400 Bad Request** - Auction not pending:
```json
{
  "error": "Auction can only be started if it is pending."
}
```

**403 Forbidden** - Not the creator:
```json
{
  "error": "Only the creator can start the auction."
}
```

---

### Stop Auction

**What this does**: Manually stops an active auction (changes status to "completed").

**Endpoint**: `POST /api/auctions/api/{auction_id}/stop/`

**Authentication Required**: Yes (Token)

**Who Can Stop**: Only the user who created the auction

**Example Request**:
```bash
curl -X POST http://localhost:8000/api/auctions/api/550e8400-e29b-41d4-a716-446655440000/stop/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

**Success Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "end_time": "2024-01-15T10:35:00Z",
  "winner_username": "john_doe",
  ...
}
```

**Note**: The last human bidder is declared as the winner.

---

### Get Auction Bids

**What this does**: Returns all bids for a specific auction.

**Endpoint**: `GET /api/auctions/api/{auction_id}/bids/`

**Authentication Required**: Yes (Token)

**Example Request**:
```bash
curl -X GET http://localhost:8000/api/auctions/api/550e8400-e29b-41d4-a716-446655440000/bids/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

**Success Response** (200 OK):
```json
[
  {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "auction": "550e8400-e29b-41d4-a716-446655440000",
    "bidder": 1,
    "bidder_username": "john_doe",
    "bidder_type": "human",
    "bidder_type_display": "Human",
    "amount": "1500.00",
    "phase": 2,
    "timestamp": "2024-01-15T10:30:00Z"
  },
  {
    "id": "660e8400-e29b-41d4-a716-446655440002",
    "auction": "550e8400-e29b-41d4-a716-446655440000",
    "bidder": null,
    "bidder_username": null,
    "bidder_type": "bot",
    "bidder_type_display": "Bot",
    "amount": "1200.00",
    "phase": 1,
    "timestamp": "2024-01-15T10:25:00Z"
  }
]
```

**Note**: Bids are ordered by timestamp (newest first).

---

### Get Auction Status Info

**What this does**: Returns detailed status information for an auction.

**Endpoint**: `GET /api/auctions/api/{auction_id}/status_info/`

**Authentication Required**: Yes (Token)

**Example Request**:
```bash
curl -X GET http://localhost:8000/api/auctions/api/550e8400-e29b-41d4-a716-446655440000/status_info/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

**Success Response** (200 OK):
```json
{
  "status": "active",
  "current_phase": 2,
  "phase_progress": 0.5,
  "remaining_time": 45.5,
  "elapsed_time": 44.5,
  "current_price": 1500.0,
  "max_bid": 10000.0,
  "bot_active": true,
  "bot_current_bid": 1200.0,
  "total_bids": 5,
  "human_bids": 3,
  "bot_bids": 2
}
```

**Use Case**: Perfect for polling to update frontend displays in real-time.

---

## Bidding Endpoints

### Place a Bid

**What this does**: Places a bid on an active auction.

**Endpoint**: `POST /api/auctions/api/{auction_id}/bid/`

**Authentication Required**: Yes (Token)

**Rate Limit**: 30 bids per minute per user

**Request Body**:
```json
{
  "amount": 1500,
  "increment": 500
}
```

**Field Details**:
- `amount` (required): Your bid amount, must be >= (current_price + minimum_increment)
- `increment` (optional): Bid increment (100, 500, or 1000). If not provided, will be calculated automatically.

**Validation Rules**:
1. Auction must be active
2. Auction must have time remaining (or be in Phase 3 with extension possible)
3. Amount must be higher than current price
4. Increment must be one of: 100, 500, 1000
5. Amount must match a valid increment from current price

**Example Request**:
```bash
curl -X POST http://localhost:8000/api/auctions/api/550e8400-e29b-41d4-a716-446655440000/bid/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 1500,
    "increment": 500
  }'
```

**Success Response** (201 Created):
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "auction": "550e8400-e29b-41d4-a716-446655440000",
  "bidder": 1,
  "bidder_username": "john_doe",
  "bidder_type": "human",
  "bidder_type_display": "Human",
  "amount": "1500.00",
  "phase": 2,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Error Responses**:

**400 Bad Request** - Invalid bid:
```json
{
  "amount": ["Bid must be at least ₹1500. Current price is ₹1000."],
  "increment": ["Increment must be one of: [100, 500, 1000]"]
}
```

**400 Bad Request** - Auction not active:
```json
{
  "non_field_errors": ["Auction is not active."]
}
```

**400 Bad Request** - Auction ended:
```json
{
  "non_field_errors": ["Auction has ended."]
}
```

**429 Too Many Requests** - Rate limit exceeded:
```json
{
  "detail": "Request was throttled. Expected available in 30 seconds."
}
```

---

### Get Active Auctions

**What this does**: Returns all currently active auctions (no authentication required).

**Endpoint**: `GET /api/auctions/api/active/`

**Authentication Required**: No

**Example Request**:
```bash
curl -X GET http://localhost:8000/api/auctions/api/active/
```

**Success Response** (200 OK):
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Vintage Watch",
    "status": "active",
    "current_price": "1500.00",
    "remaining_time": 45.5,
    ...
  }
]
```

---

### Get My Auctions

**What this does**: Returns all auctions created by the authenticated user.

**Endpoint**: `GET /api/auctions/api/my-auctions/`

**Authentication Required**: Yes (Token)

**Example Request**:
```bash
curl -X GET http://localhost:8000/api/auctions/api/my-auctions/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

**Success Response** (200 OK):
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Vintage Watch",
    "status": "pending",
    ...
  }
]
```

---

### Get My Bids

**What this does**: Returns all bids placed by the authenticated user.

**Endpoint**: `GET /api/auctions/api/my-bids/`

**Authentication Required**: Yes (Token)

**Example Request**:
```bash
curl -X GET http://localhost:8000/api/auctions/api/my-bids/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

**Success Response** (200 OK):
```json
[
  {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "auction": "550e8400-e29b-41d4-a716-446655440000",
    "amount": "1500.00",
    "phase": 2,
    "timestamp": "2024-01-15T10:30:00Z"
  }
]
```

---

## Statistics Endpoint

### Get Statistics

**What this does**: Returns comprehensive statistics about the auction system.

**Endpoint**: `GET /api/auctions/api/statistics/`

**Authentication Required**: Yes (Token)

**Example Request**:
```bash
curl -X GET http://localhost:8000/api/auctions/api/statistics/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

**Success Response** (200 OK):
```json
{
  "total_auctions": 100,
  "active_auctions": 5,
  "completed_auctions": 90,
  "total_bids": 500,
  "total_revenue": "50000.00",
  "average_bid_amount": "100.00",
  "top_bidders": [
    {
      "bidder__username": "john_doe",
      "bid_count": 25,
      "total_amount": "5000.00"
    },
    {
      "bidder__username": "jane_smith",
      "bid_count": 20,
      "total_amount": "4000.00"
    }
  ],
  "recent_auctions": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Vintage Watch",
      "status": "completed",
      "current_price": "5000.00",
      "winner_username": "john_doe",
      ...
    }
  ]
}
```

**Response Fields Explained**:
- `total_auctions`: Total number of auctions ever created
- `active_auctions`: Currently active auctions
- `completed_auctions`: Completed auctions
- `total_bids`: Total number of bids placed
- `total_revenue`: Sum of final prices of completed auctions with winners
- `average_bid_amount`: Average bid amount across all bids
- `top_bidders`: Top 10 users by number of bids
- `recent_auctions`: 5 most recently completed auctions

---

## Error Handling

### HTTP Status Codes

- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Authentication required or invalid token
- **403 Forbidden**: Permission denied
- **404 Not Found**: Resource not found
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Server error

### Error Response Format

**Single Field Error**:
```json
{
  "field_name": ["Error message here"]
}
```

**Multiple Field Errors**:
```json
{
  "field1": ["Error 1"],
  "field2": ["Error 2"]
}
```

**Non-Field Errors**:
```json
{
  "non_field_errors": ["General error message"]
}
```

**Detail Error**:
```json
{
  "detail": "Detailed error message"
}
```

### Common Error Scenarios

**Invalid Token**:
```json
{
  "detail": "Invalid token."
}
```
**Solution**: Login again to get a new token

**Permission Denied**:
```json
{
  "error": "Only the creator can start the auction."
}
```
**Solution**: Make sure you're the auction creator

**Validation Error**:
```json
{
  "amount": ["Bid must be at least ₹1500. Current price is ₹1000."]
}
```
**Solution**: Check the error message and fix your input

---

## Rate Limiting

### Rate Limits

- **Anonymous Users**: 100 requests per hour
- **Authenticated Users**: 1000 requests per hour
- **Bidding Endpoint**: 30 requests per minute

### Rate Limit Headers

Responses include rate limit information:

```
X-RateLimit-Limit: 30
X-RateLimit-Remaining: 25
X-RateLimit-Reset: 1640995200
```

**Header Explanation**:
- `X-RateLimit-Limit`: Maximum requests allowed
- `X-RateLimit-Remaining`: Requests remaining in current window
- `X-RateLimit-Reset`: Unix timestamp when limit resets

### Rate Limit Exceeded

**Response** (429 Too Many Requests):
```json
{
  "detail": "Request was throttled. Expected available in 30 seconds."
}
```

**Solution**: Wait for the specified time before making another request

---

## Example Workflows

### Complete Workflow: Create and Run an Auction

**Step 1: Register/Login**
```bash
# Register
curl -X POST http://localhost:8000/api/auth/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123"
  }'

# Save the token from response
TOKEN="your-token-here"
```

**Step 2: Create Auction**
```bash
curl -X POST http://localhost:8000/api/auctions/api/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Item",
    "description": "A test auction",
    "start_price": 1000,
    "max_bid": 10000,
    "duration": 90,
    "bot_active": true
  }'

# Save the auction ID from response
AUCTION_ID="auction-id-here"
```

**Step 3: Start Auction**
```bash
curl -X POST http://localhost:8000/api/auctions/api/$AUCTION_ID/start/ \
  -H "Authorization: Token $TOKEN"
```

**Step 4: Place Bids**
```bash
curl -X POST http://localhost:8000/api/auctions/api/$AUCTION_ID/bid/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 1500,
    "increment": 500
  }'
```

**Step 5: Check Status**
```bash
curl -X GET http://localhost:8000/api/auctions/api/$AUCTION_ID/status_info/ \
  -H "Authorization: Token $TOKEN"
```

**Step 6: View Bids**
```bash
curl -X GET http://localhost:8000/api/auctions/api/$AUCTION_ID/bids/ \
  -H "Authorization: Token $TOKEN"
```

---

## 📝 Using Swagger UI (Recommended)

**Best Way to Test the API**:

1. **Open Swagger**:
   - Go to: http://localhost:8000/swagger/

2. **Authorize**:
   - Click "Authorize" button (lock icon, top right)
   - Enter: `Token YOUR_TOKEN_HERE`
   - Click "Authorize"
   - Click "Close"

3. **Test Endpoints**:
   - Find any endpoint
   - Click to expand
   - Click "Try it out"
   - Fill in parameters
   - Click "Execute"
   - See response below

4. **Benefits**:
   - ✅ No need to write code
   - ✅ See all available endpoints
   - ✅ Automatic authentication
   - ✅ See request/response examples
   - ✅ Test immediately

---

## 🔧 Advanced Usage

### Python Example

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Register
response = requests.post(f"{BASE_URL}/auth/api/register/", json={
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123"
})
token = response.json()["token"]

# Create auction
headers = {"Authorization": f"Token {token}"}
response = requests.post(f"{BASE_URL}/auctions/api/", headers=headers, json={
    "title": "Test Auction",
    "start_price": 1000,
    "max_bid": 10000,
    "duration": 90,
    "bot_active": True
})
auction_id = response.json()["id"]

# Start auction
requests.post(f"{BASE_URL}/auctions/api/{auction_id}/start/", headers=headers)

# Place bid
requests.post(f"{BASE_URL}/auctions/api/{auction_id}/bid/", headers=headers, json={
    "amount": 1500,
    "increment": 500
})
```

### JavaScript Example

```javascript
const BASE_URL = "http://localhost:8000/api";

// Register
const registerResponse = await fetch(`${BASE_URL}/auth/api/register/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        username: "testuser",
        email: "test@example.com",
        password: "testpass123",
        password_confirm: "testpass123"
    })
});
const { token } = await registerResponse.json();

// Create auction
const headers = {
    'Authorization': `Token ${token}`,
    'Content-Type': 'application/json'
};
const auctionResponse = await fetch(`${BASE_URL}/auctions/api/`, {
    method: 'POST',
    headers,
    body: JSON.stringify({
        title: "Test Auction",
        start_price: 1000,
        max_bid: 10000,
        duration: 90,
        bot_active: true
    })
});
const { id: auctionId } = await auctionResponse.json();

// Start auction
await fetch(`${BASE_URL}/auctions/api/${auctionId}/start/`, {
    method: 'POST',
    headers
});

// Place bid
await fetch(`${BASE_URL}/auctions/api/${auctionId}/bid/`, {
    method: 'POST',
    headers,
    body: JSON.stringify({
        amount: 1500,
        increment: 500
    })
});
```

---

## 📞 Need Help?

- **Swagger UI**: http://localhost:8000/swagger/ - Interactive testing
- **Check Logs**: Look in `logs/auction.log` for detailed error messages
- **Django Admin**: http://localhost:8000/admin/ - Manage data directly
- **Documentation**: See `README.md` and `HOW_TO_RUN.md`

---

**Happy API Testing! 🚀**
