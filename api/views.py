from fastapi import APIRouter, FastAPI
from api.graph.views import router as graph_router
from api.document.views import router as document_router
#
router = APIRouter(
    responses={404: {"description": "Not found"}},
)
#
router.include_router(graph_router, prefix="/graph", tags=["graph"])
router.include_router(document_router, prefix="/document", tags=["document"])
#

@router.get("/")
async def root():
    return {"message": "Hello API!"}