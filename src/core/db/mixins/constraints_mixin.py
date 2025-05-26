from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class ConstraintsMixin:
    CheckConstraint("id != parent_id", name="ck_category_id_not_parent_id"),
    UniqueConstraint("name", "parent_id", name="uq_categories_name_level"),
    UniqueConstraint(
        "sort_order", "parent_id", name="uq_categories_sort_order_level"
    ),