import re

from core.exceptions import (
    AlreadyExistOnThisLevelError,
    SelfParentError,
    ForeignKeyConstraintViolationError,
)

MAPPINGS = [
    (
        re.compile(r"already exists"),
        AlreadyExistOnThisLevelError,
        lambda detail: {
            "field": detail.split("Key (")[1].split(",")[0],
            "data": detail.split("=(")[1].split(",")[0],
            "detail": detail,
        },
    ),
    (
        re.compile(r"not present"),
        ForeignKeyConstraintViolationError,
        lambda detail: {
            "field": detail.split("Key (")[1].split(")")[0],
            "data": detail.split("=(")[1].split(")")[0],
            "detail": detail,
        },
    ),
    (
        re.compile(r"own child"),
        ForeignKeyConstraintViolationError,
        lambda detail: {
            "field": detail.split("Key (")[1].split(")")[0],
            "data": detail.split("=(")[1].split(")")[0],
            "detail": detail,
        },
    ),
    (
        re.compile(r"id_not_parent"),
        SelfParentError,
    ),
]
