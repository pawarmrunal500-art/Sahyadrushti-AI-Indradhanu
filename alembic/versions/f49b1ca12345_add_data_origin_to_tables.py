"""Add data_origin to incidents alerts and sensor_nodes

Revision ID: f49b1ca12345
Revises: e28fead8b6b4
Create Date: 2026-11-08 02:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'f49b1ca12345'
down_revision: Union[str, Sequence[str], None] = 'e28fead8b6b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: add data_origin column."""
    with op.batch_alter_table('incidents', schema=None) as batch_op:
        batch_op.add_column(sa.Column('data_origin', sa.String(), nullable=False, server_default='demo_seed'))
        batch_op.create_index(batch_op.f('ix_incidents_data_origin'), ['data_origin'], unique=False)

    with op.batch_alter_table('alerts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('data_origin', sa.String(), nullable=False, server_default='demo_seed'))
        batch_op.create_index(batch_op.f('ix_alerts_data_origin'), ['data_origin'], unique=False)

    with op.batch_alter_table('sensor_nodes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('data_origin', sa.String(), nullable=False, server_default='demo_seed'))
        batch_op.create_index(batch_op.f('ix_sensor_nodes_data_origin'), ['data_origin'], unique=False)


def downgrade() -> None:
    """Downgrade schema: remove data_origin column."""
    with op.batch_alter_table('sensor_nodes', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_sensor_nodes_data_origin'))
        batch_op.drop_column('data_origin')

    with op.batch_alter_table('alerts', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_alerts_data_origin'))
        batch_op.drop_column('data_origin')

    with op.batch_alter_table('incidents', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_incidents_data_origin'))
        batch_op.drop_column('data_origin')
