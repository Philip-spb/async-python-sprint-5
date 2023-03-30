from typing import Optional

from pydantic import BaseModel


class PingSchema(BaseModel):
    db: Optional[int] = None
