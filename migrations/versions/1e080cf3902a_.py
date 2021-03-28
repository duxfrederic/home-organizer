"""empty message

Revision ID: 1e080cf3902a
Revises: 
Create Date: 2021-03-27 20:51:50.789024

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e080cf3902a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_timestamp'), 'user', ['timestamp'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('location',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('batiment', sa.String(length=64), nullable=True),
    sa.Column('etage', sa.Integer(), nullable=True),
    sa.Column('piece', sa.String(length=64), nullable=True),
    sa.Column('nom', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=256), nullable=True),
    sa.Column('photopath', sa.String(length=128), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('comment', sa.String(length=256), nullable=True),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('location_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('photopath', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['location_id'], ['location.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('item')
    op.drop_table('location')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_timestamp'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
