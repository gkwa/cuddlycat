import pathlib
import json
import fastapi
import fastapi.responses
from .models import Business
from pydantic import BaseModel


class PageContent(BaseModel):
    encoding: str
    mimeType: str
    data: str


class PageMetadata(BaseModel):
    url: str
    title: str
    timestamp: str
    savedAt: str
    uuid: str


class PageData(BaseModel):
    metadata: PageMetadata
    content: PageContent


def register_routes(app: fastapi.FastAPI):
    static_path = pathlib.Path(__file__).parent / "static"
    data_path = static_path / "data" / "businesses.json"

    @app.get("/api/businesses")
    async def get_businesses():
        try:
            print(f"Attempting to read from: {data_path}")
            print(f"File exists: {data_path.exists()}")
            with open(data_path, "r") as f:
                data = json.load(f)
                print(f"Successfully loaded data: {data}")
                return data
        except Exception as e:
            print(f"Error loading businesses: {str(e)}")
            raise fastapi.HTTPException(status_code=500, detail=str(e))

    @app.get("/")
    async def root():
        index_path = static_path / "index.html"
        return fastapi.responses.FileResponse(index_path)

    @app.get("/healthcheck")
    async def healthcheck():
        return {"status": "healthy"}

    @app.post("/incoming")
    async def receive_yaml(data: Business):
        try:
            print("\nReceived business data:")
            print(f"Business Name: {data.business_name}")
            print(f"Matched Name: {data.matched_name}")
            print(f"Yelp URL: {data.yelp_url}")
            print(f"Message: {data.message}")
            print(f"UUID: {data.uuid}")

            return {
                "status": "success",
                "message": "Business data received successfully",
                "data": data.model_dump(),
            }
        except Exception as e:
            print(f"Error processing business data: {str(e)}")
            raise fastapi.HTTPException(status_code=500, detail=str(e))

    @app.post("/save")
    async def save_page(data: PageData):
        try:
            print(f"\nReceived page data for URL: {data.metadata.url}")
            print(f"Title: {data.metadata.title}")
            print(f"UUID: {data.metadata.uuid}")
            return {
                "status": "success",
                "message": "Page data received successfully",
                "metadata": data.metadata.model_dump(),
            }
        except Exception as e:
            print(f"Error saving page data: {str(e)}")
            raise fastapi.HTTPException(status_code=500, detail=str(e))
