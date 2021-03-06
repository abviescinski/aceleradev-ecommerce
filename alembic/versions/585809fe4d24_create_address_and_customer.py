"""create address and customer

Revision ID: 585809fe4d24
Revises: 506264103b48
Create Date: 2021-12-07 10:27:58.877318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '585809fe4d24'
down_revision = '506264103b48'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=45), nullable=True),
    sa.Column('last_name', sa.String(length=45), nullable=True),
    sa.Column('phone_number', sa.String(length=45), nullable=True),
    sa.Column('genre', sa.String(length=45), nullable=True),
    sa.Column('cpf_cnpj', sa.String(length=45), nullable=True),
    sa.Column('birth_date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('address',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('city', sa.String(length=45), nullable=True),
    sa.Column('state', sa.String(length=2), nullable=True),
    sa.Column('number', sa.String(length=10), nullable=True),
    sa.Column('zipcode', sa.String(length=6), nullable=True),
    sa.Column('neighbourhood', sa.String(length=45), nullable=True),
    sa.Column('primary', sa.Boolean(), nullable=True),
    sa.Column('costumer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['costumer_id'], ['customer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('address')
    op.drop_table('customer')
    # ### end Alembic commands ###
