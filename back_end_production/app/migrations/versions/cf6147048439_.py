"""empty message

Revision ID: cf6147048439
Revises: 
Create Date: 2021-02-10 23:17:55.636336

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf6147048439'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sellers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('phone_number', sa.String(length=120), nullable=True),
    sa.Column('store_description', sa.Text(), nullable=True),
    sa.Column('registration_date', sa.DateTime(), nullable=False),
    sa.Column('avatar', sa.String(), nullable=True),
    sa.Column('website', sa.String(length=120), nullable=True),
    sa.Column('facebook_link', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tags',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=False),
    sa.Column('update_date', sa.DateTime(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('num_of_sales', sa.Integer(), nullable=True),
    sa.Column('total_sales', sa.Float(), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('image_url', sa.String(length=120), nullable=True),
    sa.Column('seller_id', sa.Integer(), nullable=False),
    sa.Column('cat_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cat_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['seller_id'], ['sellers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reviews',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('reviewer', sa.String(length=120), nullable=True),
    sa.Column('review', sa.Text(), nullable=False),
    sa.Column('review_date', sa.DateTime(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tag_product_association',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
    sa.PrimaryKeyConstraint('tag_id', 'product_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tag_product_association')
    op.drop_table('reviews')
    op.drop_table('products')
    op.drop_table('tags')
    op.drop_table('sellers')
    op.drop_table('categories')
    # ### end Alembic commands ###
