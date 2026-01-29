# Data Model: Authentication, Authorization & API Security

## Entities

### JWT Token
**Description**: Secure token containing user identity information with expiry validation
- **Fields**:
  - sub (subject): user_id from the user record
  - email: user's email address
  - exp: expiration timestamp
  - iat: issued at timestamp
  - jti: token identifier (optional)
- **Relationships**: Associated with a User entity via user_id
- **Validation**: Must have valid signature, not expired, and contain required claims

### Authenticated User
**Description**: User identity extracted from JWT token for authorization decisions
- **Fields**:
  - user_id: unique identifier from the token subject claim
  - email: user's email from the token
  - is_authenticated: boolean indicating successful authentication
- **Relationships**: Links to User entity in the existing data model

### Protected Resource Access
**Description**: Represents an API endpoint access attempt that requires authentication
- **Fields**:
  - resource_path: the API endpoint being accessed
  - requested_user_id: user_id from the request parameters
  - authenticated_user_id: user_id from the JWT token
  - access_granted: boolean indicating if access was permitted
- **Validation**: requested_user_id must match authenticated_user_id for user-specific resources

## Relationships
- JWT Token → User (via user_id in token subject claim)
- Authenticated User → User (via user_id mapping)
- Protected Resource Access → User (via authenticated_user_id)

## Constraints
- JWT tokens must be validated before accessing protected resources
- User-specific resources require user_id in token to match the requested user_id
- Expired tokens must be rejected regardless of other validity checks