from pydantic import BaseModel


class Catalog(BaseModel):
    id: str
    location: str
    archived: bool
    revision: int


class Catalogs(BaseModel):
    catalogs: list[Catalog]

