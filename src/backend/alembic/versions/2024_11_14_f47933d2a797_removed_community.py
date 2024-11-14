"""removed community

Revision ID: f47933d2a797
Revises: d7e348a91fe4
Create Date: 2024-11-14 09:56:14.890763

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f47933d2a797'
down_revision: Union[str, None] = 'd7e348a91fe4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('deployments', 'is_community')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('deployments', sa.Column('is_community', sa.BOOLEAN(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###