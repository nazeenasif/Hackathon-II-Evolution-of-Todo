"""Conversation and Message tables for AI chat functionality

Revision ID: 002
Revises: 001
Create Date: 2026-02-04 14:50:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create conversations table
    op.create_table(
        'conversation',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create messages table
    op.create_table(
        'message',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.Enum('user', 'assistant', 'system', 'tool', name='roleenum'), nullable=False),
        sa.Column('content', sa.String(length=10000), nullable=False),
        sa.Column('tool_calls', sa.String(length=5000), nullable=True),
        sa.Column('tool_call_results', sa.String(length=5000), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversation.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for efficient queries
    op.create_index('ix_conversation_user_id', 'conversation', ['user_id'])
    op.create_index('ix_conversation_created_at', 'conversation', ['created_at'])
    op.create_index('ix_message_conversation_id', 'message', ['conversation_id'])
    op.create_index('ix_message_role', 'message', ['role'])
    op.create_index('ix_message_created_at', 'message', ['created_at'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_message_created_at', table_name='message')
    op.drop_index('ix_message_role', table_name='message')
    op.drop_index('ix_message_conversation_id', table_name='message')
    op.drop_index('ix_conversation_created_at', table_name='conversation')
    op.drop_index('ix_conversation_user_id', table_name='conversation')

    # Drop tables
    op.drop_table('message')
    op.drop_table('conversation')