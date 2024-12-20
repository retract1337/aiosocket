from pydantic import BaseModel
from typing import Optional


class Session(BaseModel):
    session_id: str
    peername: str
    peer_ip: Optional[str] = None


# You can create your own session class by inheriting from the Session class
class CustomSession(Session):
    authorized: Optional[bool] = False
    username: Optional[str] = None

    def authorize(self, username: str) -> None:
        self.authorized = True
        self.username = username

    def unauthorize(self) -> None:
        self.authorized = False
        self.username = None
