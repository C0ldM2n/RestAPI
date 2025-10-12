"""restore users table after mistaken drop

Revision ID: 082cdb59597f
Revises: 47f3eaf54a67
Create Date: 2025-10-12 09:20:54.408546

"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "082cdb59597f"
down_revision: str | None = "3e254d725aba"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Если нужно подстраховаться от повторного запуска на БД, где таблица уже есть:
    bind = op.get_bind()
    insp = sa.inspect(bind)
    if not insp.has_table("users"):  # добавьте schema="auth" при необходимости
        op.create_table(
            "users",
            sa.Column("id", sa.UUID(), nullable=False),
            sa.Column("name", sa.String(), nullable=False),
            # Делаем NOT NULL сразу, чтобы последующий ALTER (created_at SET NOT NULL)
            # стал no-op и не падал:
            sa.Column(
                "created_at",
                postgresql.TIMESTAMP(timezone=True),
                server_default=sa.text("now()"),
                nullable=False,
            ),
            sa.Column(
                "updated_at",
                postgresql.TIMESTAMP(timezone=True),
                server_default=sa.text("now()"),
                nullable=False,
            ),
            sa.PrimaryKeyConstraint("id", name="users_pkey"),
            # schema="auth",  ← раскомментируйте и проставьте, если таблица живёт не в public
        )

        # Индекс как был в downgrade той «ломающей» ревизии:
        op.create_index("ix_users_id", "users", ["id"], unique=False)
        # Если используется схема:
        # op.create_index("ix_users_id", "users", ["id"], unique=False, schema="auth")


def downgrade() -> None:
    # Обратное действие — удалить то, что создали.
    # Если используется схема, не забудьте schema="auth"
    op.drop_index("ix_users_id", table_name="users")
    op.drop_table("users")
