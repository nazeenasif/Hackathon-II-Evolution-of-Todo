# Quickstart Guide: AI Chat Agent & Conversation System

## Overview
This guide provides essential information for developers working with the AI Chat Agent & Conversation System. This feature adds natural language task management capabilities to the existing full-stack todo application.

## Prerequisites
- Python 3.9+ with pip
- Node.js 18+ with npm
- Next.js 16+ development environment
- PostgreSQL database (Neon Serverless recommended)
- OpenAI API key
- Existing full-stack-todo application setup

## Environment Setup

### Backend Configuration
1. Add the following to your `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=your_postgresql_connection_string
```

2. Install required Python dependencies:
```bash
pip install openai sqlmodel
```

### Frontend Configuration
1. Ensure ChatKit UI components are available in your Next.js project
2. Verify authentication tokens are properly configured for API access

## Database Models

### Conversation Model
```python
# Example structure (see data-model.md for complete definition)
class Conversation(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    title: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Message Model
```python
# Example structure (see data-model.md for complete definition)
class Message(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id")
    role: str  # 'user', 'assistant', 'system', 'tool'
    content: str
    tool_calls: Optional[dict] = None
    tool_call_results: Optional[dict] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

## API Endpoints

### Chat Endpoint
- **Path**: `POST /api/chat`
- **Purpose**: Process natural language input and return AI-generated responses (authenticated via JWT)
- **Authentication**: JWT token required
- **Request Body**:
  ```json
  {
    "conversation_id": "optional-existing-conversation-id",
    "message": "user's natural language input"
  }
  ```
- **Response**:
  ```json
  {
    "conversation_id": "conversation-id-used-or-created",
    "response": "AI-generated response",
    "tool_calls": [
      {
        "tool_name": "name-of-tool-called",
        "arguments": {},
        "result": {}
      }
    ]
  }
  ```

### Conversation Management
- `GET /api/conversations` - List authenticated user's conversations
- `GET /api/conversations/{conversation_id}` - Get conversation details
- `DELETE /api/conversations/{conversation_id}` - Delete conversation

## AI Integration

### OpenAI Assistant Configuration
The system uses OpenAI's Assistants API to process user input. The assistant is configured with:
- Custom system instructions for task management
- MCP tools for interacting with the backend
- Conversation memory through thread management

### MCP Tool Integration
MCP tools are registered with the AI assistant to handle specific task operations:
- Task creation, updating, deletion, and listing
- Authentication handled transparently
- Structured input/output for reliable processing

## Frontend Integration

### Chat Modal Component
The chat interface is implemented as a modal that can be triggered from anywhere in the application:
- Accessible via a floating action button or menu option
- Shows conversation history and message input
- Displays loading states during AI processing
- Handles errors gracefully

### Message Display
Messages are displayed in chronological order with appropriate styling:
- User messages aligned right
- AI responses aligned left
- Tool calls and results displayed in a compact format
- Timestamps for context

## Development Workflow

### Adding New Features
1. Update the specification in `specs/1-ai-chat-agent/spec.md`
2. Update the implementation plan in `specs/1-ai-chat-agent/impl-plan.md`
3. Modify data models in `specs/1-ai-chat-agent/data-model.md` if needed
4. Update API contracts in `specs/1-ai-chat-agent/contracts/`
5. Implement the changes following the established patterns

### Testing
1. Unit tests for backend services
2. Integration tests for API endpoints
3. End-to-end tests for complete chat workflows
4. Error handling tests for edge cases

## Troubleshooting

### Common Issues
- **AI Processing Delays**: Check OpenAI API rate limits and consider implementing queuing
- **Authentication Failures**: Verify JWT token validity and scope
- **Database Connection Issues**: Ensure PostgreSQL connection string is correct
- **Tool Call Failures**: Check MCP tool availability and error handling

### Performance Considerations
- Monitor AI response times and implement caching for common operations if needed
- Use database indexing effectively for conversation history queries
- Implement proper error handling to prevent cascading failures

## Next Steps
1. Review the complete API documentation in `contracts/chat-api.yaml`
2. Study the implementation plan in `impl-plan.md` for detailed architecture
3. Examine the data model in `data-model.md` for database design details
4. Look at the research findings in `research.md` for design rationale