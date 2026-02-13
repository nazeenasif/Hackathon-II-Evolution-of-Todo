"""Initial tables for User and Task

Revision ID: 001
Revises:
Create Date: 2026-01-11 14:30:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )

    # Create tasks table
    op.create_table(
        'task',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(length=1000), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False),
        sa.Column('priority', sa.String(length=10), nullable=False),
        sa.Column('tags', sa.String(length=500), nullable=True),
        sa.Column('due_date', sa.DateTime(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for efficient queries
    op.create_index('ix_task_user_id', 'task', ['user_id'])
    op.create_index('ix_task_completed', 'task', ['completed'])
    op.create_index('ix_task_priority', 'task', ['priority'])
    op.create_index('ix_task_due_date', 'task', ['due_date'])
    # Composite index for combined filtering
    op.create_index('ix_task_user_completed_priority', 'task', ['user_id', 'completed', 'priority'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_task_user_completed_priority', table_name='task')
    op.drop_index('ix_task_due_date', table_name='task')
    op.drop_index('ix_task_priority', table_name='task')
    op.drop_index('ix_task_completed', table_name='task')
    op.drop_index('ix_task_user_id', table_name='task')

    # Drop tables
    op.drop_table('task')
    op.drop_table('user')