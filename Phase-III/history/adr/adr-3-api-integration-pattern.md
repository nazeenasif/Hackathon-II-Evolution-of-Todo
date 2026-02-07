# ADR-3: API Integration Pattern

## Title
API Integration Pattern: REST API Consumption with Axios Client and JWT Interceptors

## Status
Accepted

## Date
2026-01-11

## Context
We need to establish a consistent pattern for integrating the Next.js frontend with the FastAPI backend REST API. The integration must handle JWT authentication, provide error handling, support loading states, and enable efficient data fetching for task management features (CRUD operations, filtering, searching, sorting).

## Decision
We will implement the following API integration pattern:

- **HTTP Client**: Axios for making HTTP requests with promise-based API
- **JWT Interceptor**: Global request interceptor to automatically attach JWT tokens
- **Error Handling**: Consistent error response handling with user feedback
- **Service Layer**: Dedicated service modules for organizing API calls by domain
- **Response Caching**: Client-side caching where appropriate to reduce redundant requests
- **Loading States**: Consistent loading indicators for better user experience
- **Type Safety**: TypeScript interfaces matching backend models for type safety

## Alternatives Considered
1. **Fetch API**: Native browser API but requires more boilerplate for interceptors and error handling
2. **SWR**: React Hooks for data fetching but may not handle authentication as cleanly
3. **React Query**: Alternative data fetching library but axios with interceptors provides simpler JWT handling
4. **GraphQL**: Alternative to REST but would require backend changes which are not allowed per constraints
5. **Custom HTTP Wrapper**: Building from scratch but axios provides mature interceptor functionality

## Consequences
### Positive
- Axios interceptors provide clean separation of authentication logic
- Consistent error handling across all API calls
- Type safety reduces runtime errors and improves developer experience
- Well-documented and widely adopted HTTP client library
- Built-in support for request/response transformation
- Easy testing with mock adapters

### Negative
- Additional dependency beyond native fetch
- Bundle size increase from including axios library
- Learning curve for team members unfamiliar with axios patterns
- May introduce complexity for simple API calls that could use fetch
- Additional configuration needed for proper JWT token management

## References
- specs/003-frontend-integration/plan.md
- specs/003-frontend-integration/spec.md
- specs/003-frontend-integration/contracts/api-contracts.md
- backend/src/api/v1/endpoints/tasks.py