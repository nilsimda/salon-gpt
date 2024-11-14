"""

Revision ID: d7e348a91fe4
Revises: 4e3eaec553bf
Create Date: 2024-11-13 16:26:04.008602

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7e348a91fe4'
down_revision: Union[str, None] = '4e3eaec553bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('studies', sa.Column('description', sa.Text(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('studies', 'description')
    # ### end Alembic commands ###