"""seed studies

Revision ID: af1b1ef43c77
Revises: 1b366c4aa01f
Create Date: 2024-12-11 17:03:59.352688

"""
from typing import Sequence, Union

from alembic import op

from backend.database_models.seeders.studies_seeder import delete_studies, studies_seed

# revision identifiers, used by Alembic.
revision: str = 'af1b1ef43c77'
down_revision: Union[str, None] = '1b366c4aa01f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    studies_seed(op)

def downgrade() -> None:
    delete_studies(op)
