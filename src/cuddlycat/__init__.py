from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
import pathlib

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
static_path = pathlib.Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

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

@app.get("/")
async def root():
    return FileResponse(static_path / "index.html")

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

def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8080)
