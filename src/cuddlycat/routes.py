import pathlib
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

    # Add debug logging for static file serving
    print(f"Static path: {static_path}")
    print(f"Static path exists: {static_path.exists()}")
    if static_path.exists():
        print("Static directory contents:", list(static_path.glob("**/*")))

    @app.get("/")
    async def root():
        index_path = static_path / "index.html"
        print(f"Serving index from: {index_path}")
        print(f"Index exists: {index_path.exists()}")
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

            # Here you would add code to save to your storage backend
            # For now, we'll just acknowledge receipt

            return {
                "status": "success",
                "message": "Page data received successfully",
                "metadata": data.metadata.model_dump(),
            }
        except Exception as e:
            print(f"Error saving page data: {str(e)}")
            raise fastapi.HTTPException(status_code=500, detail=str(e))

    # Add route for debugging static files
    @app.get("/debug/static-files")
    async def debug_static_files():
        try:
            files = list(static_path.glob("**/*"))
            return {
                "static_path": str(static_path),
                "exists": static_path.exists(),
                "files": [str(f) for f in files],
            }
        except Exception as e:
            return {
                "error": str(e),
                "static_path": str(static_path),
                "exists": static_path.exists() if static_path else False,
            }

    # Add route to check file contents
    @app.get("/debug/file-contents/{filename:path}")
    async def debug_file_contents(filename: str):
        try:
            file_path = static_path / filename
            if not file_path.exists():
                return {"error": f"File not found: {filename}"}

            content = file_path.read_text()
            return {
                "filename": filename,
                "exists": True,
                "size": len(content),
                "content": content[:1000],  # First 1000 chars for safety
            }
        except Exception as e:
            return {"error": str(e)}
