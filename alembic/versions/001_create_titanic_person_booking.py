"""create titanic_persons and titanic_bookings

Revision ID: 001_titanic_person_booking
Revises:
Create Date: 2026-05-29

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001_titanic_person_booking"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "titanic_persons",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("passenger_id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("gender", sa.String(), nullable=False),
        sa.Column("age", sa.String(), nullable=False),
        sa.Column("sib_sp", sa.String(), nullable=False),
        sa.Column("parch", sa.String(), nullable=False),
        sa.Column("survived", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("passenger_id"),
    )
    op.create_index("ix_titanic_persons_passenger_id", "titanic_persons", ["passenger_id"])

    op.create_table(
        "titanic_bookings",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("passenger_id", sa.String(), nullable=False),
        sa.Column("pclass", sa.String(), nullable=False),
        sa.Column("ticket", sa.String(), nullable=False),
        sa.Column("fare", sa.String(), nullable=False),
        sa.Column("cabin", sa.String(), nullable=False),
        sa.Column("embarked", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["passenger_id"], ["titanic_persons.passenger_id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("passenger_id"),
    )
    op.create_index("ix_titanic_bookings_passenger_id", "titanic_bookings", ["passenger_id"])


def downgrade() -> None:
    op.drop_index("ix_titanic_bookings_passenger_id", table_name="titanic_bookings")
    op.drop_table("titanic_bookings")
    op.drop_index("ix_titanic_persons_passenger_id", table_name="titanic_persons")
    op.drop_table("titanic_persons")
