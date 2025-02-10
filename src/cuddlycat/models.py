from pydantic import BaseModel


class Content(BaseModel):
    encoding: str
    mimeType: str
    data: str


class Metadata(BaseModel):
    url: str
    title: str
    timestamp: str
    savedAt: str
    uuid: str


class YAMLData(BaseModel):
    metadata: Metadata
    content: Content
