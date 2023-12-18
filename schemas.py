from pydantic import BaseModel
from typing import List

class Reference(BaseModel):
    docName: str
    link: str
    pageNumber: str


class Resource(BaseModel):
    title: str
    _type: str
    source: str
    matrix: List
    value: str
    reference: Reference

    