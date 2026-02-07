# Data Model: AI Chat Agent Conversation System

## Entity Definitions

### Conversation
Represents a single conversation thread between a user and the AI agent.

**Fields:**
- `id`: Integer (Primary Key)
  - Type: Integer, auto-generated (using database auto-increment)
  - Purpose: Unique identifier for the conversation
- `user_id`: Integer (Foreign Key to User)
  - Type: Integer
  - Purpose: Links conversation to the owning user
  - Constraint: Must reference an existing user
- `title`: String
  - Type: VARCHAR(255)
  - Purpose: Human-readable title for the conversation
  - Default: Derived from first message or "New Conversation"
- `created_at`: DateTime
  - Type: TIMESTAMP WITH TIMEZONE
  - Purpose: Timestamp when conversation was created
  - Default: Current timestamp
- `updated_at`: DateTime
  - Type: TIMESTAMP WITH TIMEZONE
  - Purpose: Timestamp when conversation was last updated
  - Auto-updating: Yes, updates on any change

**Relationships:**
- Belongs to: User (many-to-one)
- Has many: Messages (one-to-many)

**Constraints:**
- Foreign key constraint on user_id referencing users table
- Index on user_id for efficient user-based queries

### Message
Represents individual messages within a conversation, including both user inputs and AI responses.

**Fields:**
- `id`: Integer (Primary Key)
  - Type: Integer, auto-generated (using database auto-increment)
  - Purpose: Unique identifier for the message
- `conversation_id`: Integer (Foreign Key to Conversation)
  - Type: Integer
  - Purpose: Links message to its conversation
  - Constraint: Must reference an existing conversation
- `role`: Enum
  - Type: ENUM('user', 'assistant', 'system', 'tool')
  - Purpose: Identifies the sender/type of message
  - Values: 'user' (user input), 'assistant' (AI response), 'system' (system messages), 'tool' (tool call results)
- `content`: Text
  - Type: TEXT
  - Purpose: The actual message content
  - Size: Up to database limit
- `tool_calls`: JSON
  - Type: JSONB (PostgreSQL) or JSON
  - Purpose: Stores information about tools called by the AI
  - Format: Array of tool call objects with name and arguments
  - Nullable: Yes
- `tool_call_results`: JSON
  - Type: JSONB (PostgreSQL) or JSON
  - Purpose: Stores results from tool executions
  - Format: Object with tool call IDs and results
  - Nullable: Yes
- `created_at`: DateTime
  - Type: TIMESTAMP WITH TIMEZONE
  - Purpose: Timestamp when message was created
  - Default: Current timestamp

**Relationships:**
- Belongs to: Conversation (many-to-one)

**Constraints:**
- Foreign key constraint on conversation_id referencing conversations table
- Index on conversation_id for efficient conversation-based queries
- Index on (conversation_id, created_at) for chronological message retrieval

## Validation Rules

### Conversation Validation
- user_id must reference an existing user record
- title length must be between 1 and 255 characters
- created_at must be in the past or present
- updated_at must be equal to or later than created_at

### Message Validation
- conversation_id must reference an existing conversation record
- role must be one of the allowed enum values ('user', 'assistant', 'system', 'tool')
- content must not exceed database text limits
- tool_calls must be valid JSON if provided
- tool_call_results must be valid JSON if provided
- created_at must be in the past or present

## State Transitions

### Conversation States
The Conversation entity doesn't have explicit states but follows a lifecycle:
1. Created when user initiates first chat
2. Updated when new messages are added
3. Remains active until explicitly deleted by user
4. Deleted permanently when user chooses to delete

### Message States
Messages are immutable once created:
1. Created with initial content and role
2. Cannot be modified after creation (append-only model)
3. Associated with a specific conversation for its lifetime

## Indexing Strategy

### Required Indexes
- conversations.user_id: For efficient user-based queries
- messages.conversation_id: For efficient conversation-based queries
- messages.conversation_id_created_at: For chronological message retrieval
- conversations.updated_at: For efficient sorting by recency

### Performance Considerations
- Use integer auto-increment IDs for primary keys (consistent with existing system)
- JSONB fields for flexible tool call storage in PostgreSQL
- Composite indexes for common query patterns
- Efficient pagination for large conversation histories

## Security Considerations

### Data Isolation
- Foreign key constraints ensure messages belong to valid conversations
- Conversation ownership ensures users can only access their own conversations
- Authentication required for all access to conversation data
- Integer-based user ID validation ensures proper access control

### Privacy
- Message content stored encrypted at rest if privacy regulations require
- No personally identifiable information stored inappropriately
- Audit trail maintained for access to conversation data