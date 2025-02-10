import fastapi
import fastapi.middleware.cors
import fastapi.staticfiles
import pathlib
import uvicorn

from .routes import register_routes

app = fastapi.FastAPI()

# Enable CORS
app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
static_path = pathlib.Path(__file__).parent / "static"
app.mount(
    "/static",
    fastapi.staticfiles.StaticFiles(directory=str(static_path)),
    name="static",
)

register_routes(app)


def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8080)
