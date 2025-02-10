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
        try:
            print("Received YAML data:")
            print(f"URL: {data.metadata.url}")
            print(f"Title: {data.metadata.title}")
            print(f"Timestamp: {data.metadata.timestamp}")
            print(f"Saved At: {data.metadata.savedAt}")
            print(f"UUID: {data.metadata.uuid}")
            print(f"Content Type: {data.content.mimeType}")
            
            # Here you would add your actual data processing
            # If something goes wrong, raise an exception
            
            return {"status": "success", "message": "Data received and processed successfully"}
        except Exception as e:
            raise fastapi.HTTPException(status_code=500, detail=str(e))

