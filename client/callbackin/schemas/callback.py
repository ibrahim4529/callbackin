from typing import NamedTuple, Optional


class Callback(NamedTuple):
    name: str
    local_endpoint: str
    path: str
    id: int
    user_id: int
    is_running: bool
    description: Optional[str] = None
