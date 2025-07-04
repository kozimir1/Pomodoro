"""yandex access token

Revision ID: 40cc1b4f0dca
Revises: 17f0ecf3418b
Create Date: 2025-05-28 21:47:46.380114

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '40cc1b4f0dca'
down_revision: Union[str, None] = '17f0ecf3418b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('UserProfile', sa.Column('yandex_access_token', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('UserProfile', 'yandex_access_token')
    # ### end Alembic commands ###
