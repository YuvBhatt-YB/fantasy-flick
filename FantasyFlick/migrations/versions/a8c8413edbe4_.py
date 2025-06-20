"""empty message

Revision ID: a8c8413edbe4
Revises: 
Create Date: 2025-06-16 20:16:34.098531

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8c8413edbe4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('matches',
    sa.Column('match_id', sa.Integer(), nullable=False),
    sa.Column('match_name', sa.String(), nullable=True),
    sa.Column('series_name', sa.String(), nullable=True),
    sa.Column('team1', sa.String(), nullable=True),
    sa.Column('team2', sa.String(), nullable=True),
    sa.Column('team1_short', sa.String(), nullable=True),
    sa.Column('team2_short', sa.String(), nullable=True),
    sa.Column('start_time', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('match_id')
    )
    op.create_table('users',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.Column('wallet_balance', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('uid'),
    sa.UniqueConstraint('username')
    )
    op.create_table('contests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('match_id', sa.Integer(), nullable=False),
    sa.Column('entry_fee', sa.Integer(), nullable=False),
    sa.Column('max_participants', sa.Integer(), nullable=False),
    sa.Column('prize_pool', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['match_id'], ['matches.match_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('players',
    sa.Column('player_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('team', sa.String(), nullable=True),
    sa.Column('base_value', sa.Integer(), nullable=True),
    sa.Column('match_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['match_id'], ['matches.match_id'], ),
    sa.PrimaryKeyConstraint('player_id')
    )
    op.create_table('fantasy_team',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('team_name', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('match_id', sa.Integer(), nullable=False),
    sa.Column('captain_id', sa.Integer(), nullable=False),
    sa.Column('vice_captain_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['captain_id'], ['players.player_id'], ),
    sa.ForeignKeyConstraint(['match_id'], ['matches.match_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.uid'], ),
    sa.ForeignKeyConstraint(['vice_captain_id'], ['players.player_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fantasy_team_player',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fantasy_team_id', sa.Integer(), nullable=False),
    sa.Column('player_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['fantasy_team_id'], ['fantasy_team.id'], ),
    sa.ForeignKeyConstraint(['player_id'], ['players.player_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_contests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('contest_id', sa.Integer(), nullable=False),
    sa.Column('fantasy_team_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['contest_id'], ['contests.id'], ),
    sa.ForeignKeyConstraint(['fantasy_team_id'], ['fantasy_team.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.uid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_contests')
    op.drop_table('fantasy_team_player')
    op.drop_table('fantasy_team')
    op.drop_table('players')
    op.drop_table('contests')
    op.drop_table('users')
    op.drop_table('matches')
    # ### end Alembic commands ###
