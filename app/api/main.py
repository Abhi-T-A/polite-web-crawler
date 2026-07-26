from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers.books import router as books_router

app = FastAPI(
    title="Polite Scraper REST API",
    description="Production-grade REST API serving scraped e-commerce book data, statistics, and filtering capabilities.",
    version="2.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(books_router, prefix="/api/v1", tags=["Books"])
app.include_router(books_router, prefix="", tags=["Legacy Endpoints"])


@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "online",
        "service": "Polite Scraper REST API",
        "docs_url": "/docs",
    }
