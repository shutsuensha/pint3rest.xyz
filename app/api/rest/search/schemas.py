from pydantic import BaseModel

class SearchQueryModel(BaseModel):
    query: str