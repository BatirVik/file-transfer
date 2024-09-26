from fastapi import APIRouter
from . import files

router = APIRouter(prefix="/v1")
router.include_router(files.router)
