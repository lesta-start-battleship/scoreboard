"""Initial

Revision ID: b70581b0351b
Revises: 
Create Date: 2025-07-09 00:55:18.575971

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b70581b0351b'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('guild',
    sa.Column('guild_id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('tag', sa.String(), nullable=False),
    sa.Column('players', sa.Integer(), nullable=False),
    sa.Column('wins', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('guild_id')
    )
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('guild_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('gold', sa.Integer(), nullable=False),
    sa.Column('experience', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('containers', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['guild_id'], ['guild.guild_id'], ),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('war_result',
    sa.Column('war_id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('attacker_id', sa.Integer(), nullable=False),
    sa.Column('defender_id', sa.Integer(), nullable=False),
    sa.Column('attacker_score', sa.Integer(), nullable=False),
    sa.Column('defender_score', sa.Integer(), nullable=False),
    sa.Column('winner_id', sa.Integer(), nullable=True),
    sa.Column('winner_tag', sa.String(), nullable=True),
    sa.Column('loser_id', sa.Integer(), nullable=True),
    sa.Column('loser_tag', sa.String(), nullable=True),
    sa.Column('correlation_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['attacker_id'], ['guild.guild_id'], ),
    sa.ForeignKeyConstraint(['defender_id'], ['guild.guild_id'], ),
    sa.PrimaryKeyConstraint('war_id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('war_result')
    op.drop_table('user')
    op.drop_table('guild')
