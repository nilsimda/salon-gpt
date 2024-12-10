"""init

Revision ID: 1740614c04bc
Revises: 
Create Date: 2024-12-09 15:41:31.321084

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1740614c04bc'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blacklist',
    sa.Column('token_id', sa.String(), nullable=False),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('blacklist_token_id', 'blacklist', ['token_id'], unique=False)
    op.create_table('files',
    sa.Column('user_id', sa.String(), nullable=True),
    sa.Column('file_name', sa.String(), nullable=False),
    sa.Column('file_size', sa.Integer(), nullable=False),
    sa.Column('file_content', sa.String(), nullable=False),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('groups',
    sa.Column('display_name', sa.String(), nullable=False),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('display_name', name='unique_display_name')
    )
    op.create_table('studies',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('ti_files', sa.Text(), nullable=True),
    sa.Column('gd_files', sa.Text(), nullable=True),
    sa.Column('memo_files', sa.Text(), nullable=True),
    sa.Column('metadata_file', sa.Text(), nullable=True),
    sa.Column('is_being_added', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name', name='_study_name_uc')
    )
    op.create_table('users',
    sa.Column('user_name', sa.String(), nullable=True),
    sa.Column('fullname', sa.String(), nullable=False),
    sa.Column('external_id', sa.String(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.LargeBinary(), nullable=True),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email', name='unique_user_email'),
    sa.UniqueConstraint('user_name', name='unique_user_name')
    )
    op.create_table('conversations',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('is_pinned', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', 'user_id', name='conversation_pkey'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('id', 'user_id', name='conversation_id_user_id')
    )
    op.create_index('conversation_user_agent_index', 'conversations', ['user_id'], unique=False)
    op.create_index('conversation_user_id_index', 'conversations', ['id', 'user_id'], unique=True)
    op.create_table('interviews',
    sa.Column('interview_id', sa.String(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('interview_class', sa.String(), nullable=False),
    sa.Column('fields', sa.JSON(), nullable=True),
    sa.Column('study_id', sa.String(), nullable=False),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['study_id'], ['studies.id'], ),
    sa.PrimaryKeyConstraint('interview_id', 'id'),
    sa.UniqueConstraint('interview_id')
    )
    op.create_table('user_group',
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('group_id', sa.String(), nullable=False),
    sa.Column('display', sa.String(), nullable=False),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'group_id', 'id')
    )
    op.create_table('conversation_files',
    sa.Column('conversation_id', sa.String(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('file_id', sa.String(), nullable=False),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('conversation_id', 'file_id', name='unique_conversation_file')
    )
    op.create_table('messages',
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.Column('conversation_id', sa.String(), nullable=True),
    sa.Column('position', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('generation_id', sa.String(), nullable=True),
    sa.Column('agent', sa.Enum('USER', 'CHATBOT', name='messageagent', native_enum=False), nullable=False),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['conversation_id', 'user_id'], ['conversations.id', 'conversations.user_id'], name='message_conversation_id_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('message_conversation_id', 'messages', ['conversation_id'], unique=False)
    op.create_index('message_conversation_id_user_id', 'messages', ['conversation_id', 'user_id'], unique=False)
    op.create_index('message_is_active', 'messages', ['is_active'], unique=False)
    op.create_index('message_user_id', 'messages', ['user_id'], unique=False)
    op.create_table('citations',
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.Column('start', sa.Integer(), nullable=False),
    sa.Column('end', sa.Integer(), nullable=False),
    sa.Column('message_id', sa.String(), nullable=False),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['message_id'], ['messages.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('message_files',
    sa.Column('message_id', sa.String(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('file_id', sa.String(), nullable=False),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['message_id'], ['messages.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('message_id', 'file_id', name='unique_message_file')
    )
    op.create_index('message_file_file_id', 'message_files', ['file_id'], unique=False)
    op.create_table('snapshots',
    sa.Column('user_id', sa.String(), nullable=True),
    sa.Column('conversation_id', sa.String(), nullable=False),
    sa.Column('last_message_id', sa.String(), nullable=False),
    sa.Column('version', sa.Integer(), nullable=False),
    sa.Column('snapshot', sa.JSON(), nullable=False),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['conversation_id', 'user_id'], ['conversations.id', 'conversations.user_id'], name='snapshot_conversation_id_user_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['last_message_id'], ['messages.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('snapshot_conversation_id', 'snapshots', ['conversation_id'], unique=False)
    op.create_index('snapshot_last_message_id', 'snapshots', ['last_message_id'], unique=False)
    op.create_index('snapshot_user_id', 'snapshots', ['user_id'], unique=False)
    op.create_table('snapshot_links',
    sa.Column('snapshot_id', sa.String(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['snapshot_id'], ['snapshots.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('snapshot_link_snapshot_id', 'snapshot_links', ['snapshot_id'], unique=False)
    op.create_table('snapshot_access',
    sa.Column('user_id', sa.String(), nullable=True),
    sa.Column('snapshot_id', sa.String(), nullable=False),
    sa.Column('link_id', sa.String(), nullable=False),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['link_id'], ['snapshot_links.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['snapshot_id'], ['snapshots.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('snapshot_access_link_id', 'snapshot_access', ['link_id'], unique=False)
    op.create_index('snapshot_access_user_id', 'snapshot_access', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('snapshot_access_user_id', table_name='snapshot_access')
    op.drop_index('snapshot_access_link_id', table_name='snapshot_access')
    op.drop_table('snapshot_access')
    op.drop_index('snapshot_link_snapshot_id', table_name='snapshot_links')
    op.drop_table('snapshot_links')
    op.drop_index('snapshot_user_id', table_name='snapshots')
    op.drop_index('snapshot_last_message_id', table_name='snapshots')
    op.drop_index('snapshot_conversation_id', table_name='snapshots')
    op.drop_table('snapshots')
    op.drop_index('message_file_file_id', table_name='message_files')
    op.drop_table('message_files')
    op.drop_table('citations')
    op.drop_index('message_user_id', table_name='messages')
    op.drop_index('message_is_active', table_name='messages')
    op.drop_index('message_conversation_id_user_id', table_name='messages')
    op.drop_index('message_conversation_id', table_name='messages')
    op.drop_table('messages')
    op.drop_table('conversation_files')
    op.drop_table('user_group')
    op.drop_table('interviews')
    op.drop_index('conversation_user_id_index', table_name='conversations')
    op.drop_index('conversation_user_agent_index', table_name='conversations')
    op.drop_table('conversations')
    op.drop_table('users')
    op.drop_table('studies')
    op.drop_table('groups')
    op.drop_table('files')
    op.drop_index('blacklist_token_id', table_name='blacklist')
    op.drop_table('blacklist')
    # ### end Alembic commands ###