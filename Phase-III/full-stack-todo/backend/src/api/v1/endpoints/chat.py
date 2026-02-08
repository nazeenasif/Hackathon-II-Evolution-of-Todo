from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional, Dict, Any
from sqlmodel import Session
from pydantic import BaseModel
import uuid
from datetime import datetime
import json
from src.ai_providers.provider_factory import get_default_provider
from src.ai_providers.base_provider import ToolCall as ProviderToolCall
from src.models.conversation import Conversation, ConversationCreate
from src.models.message import Message, MessageCreate, RoleEnum
from src.services.conversation_service import ConversationService
from src.services.message_service import MessageService
from src.services.history_service import HistoryService
from src.core.security import get_current_user_id
from src.core.database import get_async_session
from src.services.task_creation_tool import run as task_create_run
from src.services.task_listing_tool import run as task_list_run

# Import other task tools as needed
try:
    from ...services.task_update_tool import run as task_update_run
except ImportError:
    task_update_run = None

try:
    from ...services.task_deletion_tool import run as task_delete_run
except ImportError:
    task_delete_run = None

try:
    from ...services.task_completion_tool import run as task_complete_run
except ImportError:
    task_complete_run = None

router = APIRouter()


class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str


class ToolCall(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]
    result: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    tool_calls: List[ToolCall]


def get_available_tools():
    """
    Get the available tools for the AI assistant.
    """
    tools = []

    # Task creation tool
    if hasattr(__import__('src.services.task_creation_tool', fromlist=['run']), 'run'):
        tools.append({
            "type": "function",
            "function": {
                "name": "create_task",
                "description": "Create a new task with title, description, priority, tags, and due date",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Title of the task"
                        },
                        "description": {
                            "type": "string",
                            "description": "Detailed description of the task"
                        },
                        "priority": {
                            "type": "string",
                            "enum": ["high", "medium", "low"],
                            "description": "Priority level of the task",
                            "default": "medium"
                        },
                        "tags": {
                            "type": "string",
                            "description": "Comma-separated tags for the task (e.g., 'work,important')"
                        },
                        "due_date": {
                            "type": "string",
                            "format": "date-time",
                            "description": "Due date for the task in ISO format (YYYY-MM-DDTHH:MM:SS.sssZ)"
                        }
                    },
                    "required": ["title"]
                }
            }
        })

    # Task listing tool
    if hasattr(__import__('src.services.task_listing_tool', fromlist=['run']), 'run'):
        tools.append({
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "List tasks with optional filtering by completion status, priority, tags, or search terms",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "completed": {
                            "type": "boolean",
                            "description": "Filter by completion status (true for completed, false for pending)"
                        },
                        "priority": {
                            "type": "string",
                            "enum": ["high", "medium", "low"],
                            "description": "Filter by priority level"
                        },
                        "tag": {
                            "type": "string",
                            "description": "Filter by specific tag"
                        },
                        "search": {
                            "type": "string",
                            "description": "Search term for title or description"
                        },
                        "sort_by": {
                            "type": "string",
                            "enum": ["due_date", "priority", "title"],
                            "description": "Field to sort by",
                            "default": "due_date"
                        },
                        "order": {
                            "type": "string",
                            "enum": ["asc", "desc"],
                            "description": "Sort order",
                            "default": "asc"
                        }
                    }
                }
            }
        })

    # Task deletion tool
    if hasattr(__import__('src.services.task_deletion_tool', fromlist=['run']), 'run'):
        tools.append({
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "Delete an existing task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "integer",
                            "description": "ID of the task to delete (optional if title is provided)"
                        },
                        "title": {
                            "type": "string",
                            "description": "Title of the task to delete (optional if task_id is provided)"
                        }
                    },
                    "required": []  # Neither field is strictly required, but one should be provided
                }
            }
        })

    # Task update tool
    if hasattr(__import__('src.services.task_update_tool', fromlist=['run']), 'run'):
        tools.append({
            "type": "function",
            "function": {
                "name": "update_task",
                "description": "Update an existing task with new information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "integer",
                            "description": "ID of the task to update (optional if title is provided)"
                        },
                        "title": {
                            "type": "string",
                            "description": "Updated title of the task (optional if task_id is provided) or title of task to update"
                        },
                        "description": {
                            "type": "string",
                            "description": "Updated detailed description of the task"
                        },
                        "priority": {
                            "type": "string",
                            "enum": ["high", "medium", "low"],
                            "description": "Updated priority level of the task"
                        },
                        "tags": {
                            "type": "string",
                            "description": "Updated comma-separated tags for the task (e.g., 'work,important')"
                        },
                        "due_date": {
                            "type": "string",
                            "format": "date-time",
                            "description": "Updated due date for the task in ISO format (YYYY-MM-DDTHH:MM:SS.sssZ)"
                        }
                    },
                    "required": []
                }
            }
        })

    # Task completion toggle tool
    if hasattr(__import__('src.services.task_completion_tool', fromlist=['run']), 'run'):
        tools.append({
            "type": "function",
            "function": {
                "name": "toggle_task_completion",
                "description": "Toggle the completion status of a task (mark as complete/incomplete)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "integer",
                            "description": "ID of the task to toggle completion status (optional if title is provided)"
                        },
                        "title": {
                            "type": "string",
                            "description": "Title of the task to toggle completion status (optional if task_id is provided)"
                        },
                        "completed": {
                            "type": "boolean",
                            "description": "Whether the task should be marked as completed (true) or not (false)"
                        }
                    },
                    "required": []
                }
            }
        })

    return tools


def execute_tool(tool_name: str, arguments: Dict[str, Any], user_id: int) -> Dict[str, Any]:
    """
    Execute the specified tool with the given arguments.
    """
    try:
        # Convert arguments to JSON string for the tool
        args_json = json.dumps(arguments)

        # Execute the appropriate tool based on name
        if tool_name == "create_task":
            # Import here to avoid circular dependencies
            from src.services.task_creation_tool import run as task_create_run
            result = task_create_run(user_id, args_json)
        elif tool_name == "list_tasks":
            from src.services.task_listing_tool import run as task_list_run
            result = task_list_run(user_id, args_json)
        elif tool_name == "update_task":
            try:
                from src.services.task_update_tool import run as task_update_run
                if task_update_run:
                    result = task_update_run(user_id, args_json)
                else:
                    return {"error": "Update task tool not available", "success": False}
            except ImportError:
                return {"error": "Update task tool not available", "success": False}
        elif tool_name == "delete_task":
            try:
                from src.services.task_deletion_tool import run as task_delete_run
                if task_delete_run:
                    result = task_delete_run(user_id, args_json)
                else:
                    return {"error": "Delete task tool not available", "success": False}
            except ImportError:
                return {"error": "Delete task tool not available", "success": False}
        elif tool_name == "toggle_task_completion":
            try:
                from src.services.task_completion_tool import run as task_complete_run
                if task_complete_run:
                    result = task_complete_run(user_id, args_json)
                else:
                    return {"error": "Toggle task completion tool not available", "success": False}
            except ImportError:
                return {"error": "Toggle task completion tool not available", "success": False}
        else:
            return {
                "error": f"Unknown tool: {tool_name}",
                "success": False
            }

        # Parse the result from JSON string
        if isinstance(result, str):
            return json.loads(result)
        else:
            return result
    except Exception as e:
        return {
            "error": f"Error executing tool {tool_name}: {str(e)}",
            "success": False
        }


@router.post("/chat", response_model=ChatResponse)
def process_chat(
    chat_request: ChatRequest,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_async_session)
):
    """
    Process a chat message and return an AI response.
    """
    try:
        # Get or create conversation
        conversation_id = chat_request.conversation_id

        if conversation_id:
            # Try to get existing conversation
            try:
                conversation_uuid = uuid.UUID(conversation_id)
            except ValueError:
                # If conversation_id is not a valid UUID, treat as integer ID
                conversation_uuid = None

            # For simplicity in this implementation, we'll create a new conversation for each request
            # In a real implementation, you'd need a mapping between UUID and integer IDs
            conversation = None
        else:
            # Create new conversation
            conversation_data = ConversationCreate(
                user_id=current_user_id,
                title=f"Chat {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
            )
            conversation = ConversationService.create_conversation(session, conversation_data)
            conversation_id = str(conversation.id)  # Using integer ID as string for now

        # Create user message
        user_message = MessageCreate(
            conversation_id=int(conversation_id) if conversation_id and conversation_id.isdigit() else 1,  # Fallback for demo
            role=RoleEnum.user,
            content=chat_request.message
        )

        # In a real implementation, we'd need to properly map UUIDs to integer IDs
        # For now, using a simple approach to save the message
        try:
            saved_message = MessageService.create_message(session, user_message)
        except:
            # If conversation ID doesn't exist, create a new one
            conversation_data = ConversationCreate(
                user_id=current_user_id,
                title=f"Chat {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
            )
            conversation = ConversationService.create_conversation(session, conversation_data)
            user_message.conversation_id = conversation.id
            saved_message = MessageService.create_message(session, user_message)
            conversation_id = str(conversation.id)

        # Prepare messages for the AI assistant with conversation history
        # Retrieve recent conversation history for context
        try:
            conversation_history = HistoryService.get_recent_conversation_history(
                session,
                int(conversation_id) if conversation_id and conversation_id.isdigit() else 1,
                current_user_id,
                limit=10  # Get last 10 messages for context
            )

            # Format conversation history as messages for the AI
            history_messages = []
            for msg in conversation_history:
                role = msg.role.value if isinstance(msg.role, RoleEnum) else msg.role
                history_messages.append({
                    "role": role,
                    "content": msg.content
                })
        except:
            # If there's an issue with history, just use empty history
            history_messages = []

        # Add system message and user's current message
        messages = [
            {"role": "system", "content": "You are a helpful assistant that helps users manage tasks. Use the available functions to create, list, update, or manage tasks."},
        ] + history_messages + [
            {"role": "user", "content": chat_request.message}
        ]

        # Get available tools
        tools = get_available_tools()

        # Get AI provider based on configuration
        ai_provider = get_default_provider()

        # Call AI provider API with tools
        response = ai_provider.chat_completion(
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        # Process the response
        response_content = response.content
        provider_tool_calls = response.tool_calls

        # Execute any tool calls
        executed_tools = []
        if provider_tool_calls:
            for tool_call in provider_tool_calls:
                function_name = tool_call.name
                function_args = tool_call.arguments

                # Execute the tool
                result = execute_tool(function_name, function_args, current_user_id)

                executed_tool = ToolCall(  # Using the Pydantic model defined in this file
                    tool_name=function_name,
                    arguments=function_args,
                    result=result
                )
                executed_tools.append(executed_tool)

                # Add tool result to messages for follow-up (if needed)
                messages.append({
                    "role": "tool",
                    "name": function_name,
                    "content": json.dumps(result)
                })

        # If there are tool results, get a final response from the AI
        final_response_content = response_content
        if executed_tools:
            # Get a follow-up response from the AI incorporating tool results
            follow_up_messages = messages + [{"role": "user", "content": "Based on the tool results, provide a helpful response to the user."}]
            follow_up_response = ai_provider.chat_completion(
                messages=follow_up_messages
            )
            final_response_content = follow_up_response.content

        # Create AI response message
        ai_message = MessageCreate(
            conversation_id=int(conversation_id) if conversation_id and conversation_id.isdigit() else 1,
            role=RoleEnum.assistant,
            content=final_response_content or "I processed your request."
        )

        try:
            ai_saved_message = MessageService.create_message(session, ai_message)
        except:
            # Handle case where conversation ID isn't valid
            ai_message.conversation_id = int(conversation_id) if conversation_id and conversation_id.isdigit() else 1
            ai_saved_message = MessageService.create_message(session, ai_message)

        # Update conversation title if it's the first message
        # Check if this is the first exchange in the conversation
        try:
            conv_id = int(conversation_id) if conversation_id and conversation_id.isdigit() else 1
            conversation = ConversationService.get_conversation_by_id(session, conv_id, current_user_id)
            if conversation and conversation.title.startswith("Chat "):
                # Get all messages for this conversation to check if this is the first exchange
                all_messages = HistoryService.get_full_conversation_history(session, conversation.id, current_user_id)
                if len(all_messages) <= 2:  # Just the user message and AI response
                    # Generate a title based on the first user message
                    new_title = chat_request.message[:50] + "..." if len(chat_request.message) > 50 else chat_request.message
                    ConversationService.update_conversation_title(session, conversation.id, current_user_id, new_title)
        except:
            # If there's an issue with conversation retrieval, continue without updating title
            pass

        # Return the response
        return ChatResponse(
            conversation_id=conversation_id,
            response=final_response_content or "I processed your request.",
            tool_calls=executed_tools
        )

    except Exception as e:
        print(f"Error in process_chat: {e}")  # For debugging
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat request: {str(e)}"
        )