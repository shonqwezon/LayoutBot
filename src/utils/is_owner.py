import os

owner_ids = os.getenv("OWNERS", "").split(",")


def is_owner(tg_id) -> bool:
    return str(tg_id).strip() in owner_ids
