from app.crud.entry import (
    create_entry,
    delete_entry,
    get_all_entries,
    get_entry,
    update_entry,
)
from app.crud.user import get_user_by_email, get_user_by_id

# Re-export CRUD functions for easier import
__all__ = [
    "create_entry",
    "delete_entry",
    "get_all_entries",
    "get_entry",
    "update_entry",
    "get_user_by_email",
    "get_user_by_id",
]
