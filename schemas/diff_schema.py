from pydantic import BaseModel
from typing import Optional

class DiffResult(BaseModel):
    title: str
    description: Optional[str] = None
    link: str
    missing_in_japan: bool
