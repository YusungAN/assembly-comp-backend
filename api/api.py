from fastapi import APIRouter
from api.endpoint import search

api_router = APIRouter()
api_router.include_router(search.router, tags=["search"])