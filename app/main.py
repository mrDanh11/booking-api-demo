from fastapi import FastAPI

from app.routers.booking_router import router as booking_router

app = FastAPI(
    title="Shipping Booking Information API",
    description="API for managing shipping booking information.",
    version="1.0.0",
)

app.include_router(booking_router)

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}
