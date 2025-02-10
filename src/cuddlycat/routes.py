import pathlib
import fastapi
import fastapi.responses

from .models import YAMLData


def register_routes(app: fastapi.FastAPI):
    static_path = pathlib.Path(__file__).parent / "static"

    @app.get("/")
    async def root():
        return fastapi.responses.FileResponse(static_path / "index.html")

    @app.post("/incoming")
    async def receive_yaml(data: YAMLData):
        print("Received YAML data:")
        print(f"URL: {data.metadata.url}")
        print(f"Title: {data.metadata.title}")
        print(f"Timestamp: {data.metadata.timestamp}")
        print(f"Saved At: {data.metadata.savedAt}")
        print(f"UUID: {data.metadata.uuid}")
        print(f"Content Type: {data.content.mimeType}")

        return {"status": "success", "message": "Data received successfully"}
