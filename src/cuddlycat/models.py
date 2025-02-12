from pydantic import BaseModel


class Business(BaseModel):
    business_name: str
    matched_name: str
    yelp_url: str
    message: str
    uuid: str
