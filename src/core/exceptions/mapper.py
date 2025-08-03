import re

from core.exceptions import (
    ForeignKeyViolationError,
    AlreadyExistsError,
)


def _parse_unique_violation(detail: str):
    """Parsing error UNIQUE constraint."""

    table_name = "unknown"

    # Method 1: Try to find an explicit 'on table "..."'
    table_match = re.search(r'on table "(.*?)"', detail)
    if table_match:
        table_name = table_match.group(1)
    else:
        # Method 2: If that doesn't work, parse the name of the constraint
        constraint_match = re.search(
            r'violates unique constraint "(.*?)"', detail
        )
        if constraint_match:
            constraint_name = constraint_match.group(1)
            # We expect the convention ‘uq_tablename_fields’ or ‘tablename_..._key’
            parts = constraint_name.split("_")
            if len(parts) > 1:
                # If the prefix is ‘uq’ or ‘ix’, take the second part
                if parts[0] in ("uq", "ix"):
                    table_name = parts[1]
                # Otherwise, we take the first part (for the ‘tablename_pkey’ convention)
                else:
                    table_name = parts[0]

    key_match = re.search(r"Key \((.*?)\)=\((.*?)\) already exists\.", detail)
    if not key_match:
        return None

    columns, values = key_match.groups()

    return {
        "entity_name": table_name.capitalize(),
        "field": columns.split(",")[
            0
        ].strip(),  # Take the first field for simplicity's sake
        "value": values.split(",")[0].strip(),
    }


def _parse_foreign_key_violation(detail: str):
    """Parsing error FOREIGN KEY constraint."""
    match = re.search(
        r'Key \((.*?)\)=\((.*?)\) is not present in table "(.*?)".', detail
    )
    if not match:
        return None

    columns, values, _ = match.groups()
    table_match = re.search(r'on table "(.*?)"', detail)
    table_name = table_match.group(1) if table_match else "unknown"

    return {
        "entity_name": table_name.capitalize(),
        "field": columns.strip(),
        "value": values.strip(),
    }


# Now it stores (regex, error class, parser function)
MAPPINGS = [
    (
        re.compile(r"violates unique constraint"),
        AlreadyExistsError,
        _parse_unique_violation,
    ),
    (
        re.compile(r"violates foreign key constraint"),
        ForeignKeyViolationError,
        _parse_foreign_key_violation,
    ),
]
