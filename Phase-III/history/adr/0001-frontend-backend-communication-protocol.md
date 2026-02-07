# ADR: Frontend-Backend Communication Protocol for Local Development

## Status
Accepted

## Context
During development of the full-stack todo application, we encountered a "Failed to fetch" error when attempting to register new users. Investigation revealed that the frontend was configured to communicate with the backend using HTTPS protocol, while the backend was running on HTTP.

## Decision
We decided to use HTTP protocol for local development communication between the frontend and backend services. This ensures consistent protocol matching between the client (frontend) and server (backend) applications.

## Rationale
1. Local development environments typically don't require the overhead of SSL/TLS encryption
2. Using HTTP simplifies the development setup process
3. The backend (FastAPI) was configured to run on HTTP by default
4. Consistent protocol matching prevents CORS and fetch errors

## Consequences
### Positive
- Eliminates "Failed to fetch" errors in local development
- Simplifies the development environment setup
- Ensures reliable frontend-backend communication

### Negative
- HTTP is not suitable for production environments
- Requires separate configuration management for different environments

## Implementation
Updated NEXT_PUBLIC_API_BASE_URL in frontend/.env.local from https://localhost:8000 to http://localhost:8000