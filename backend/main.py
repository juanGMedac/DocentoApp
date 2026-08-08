from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import grupos

app = FastAPI(
    title="DocentoApp Backend",
    description="Backend de DocentoApp con FastAPI y Oracle",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(grupos.router)

@app.get("/api/status")
def status():
    return {
        "status": "ok",
        "message": "El servidor backend de DocentoApp está funcionando correctamente."
    }
