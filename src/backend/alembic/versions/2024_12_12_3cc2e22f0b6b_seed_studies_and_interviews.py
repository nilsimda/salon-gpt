"""seed studies and interviews

Revision ID: 3cc2e22f0b6b
Revises: 23e25008ba7a
Create Date: 2024-12-12 11:00:57.795012

"""

from typing import Sequence, Union

from alembic import op

from backend.database_models.seeders.studies_seeder import delete_studies, studies_seed

# revision identifiers, used by Alembic.
revision: str = "3cc2e22f0b6b"
down_revision: Union[str, None] = "23e25008ba7a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    studies_seed(op)


def downgrade() -> None:
    delete_studies(op)

