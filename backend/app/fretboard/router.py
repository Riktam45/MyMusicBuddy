from fastapi import APIRouter, Depends

from app.ai.fretboard_schema import (
    FretboardRequest,
    FretboardResult,
)
from app.ai.fretboard_service import (
    get_scale_fretboard,
)
from app.auth.dependencies import current_user


router = APIRouter(
    prefix="/fretboard",
    tags=["Fretboard"],
)


@router.post(
    "",
    response_model=FretboardResult,
)
def get_fretboard(
    request: FretboardRequest,
    user=Depends(current_user),
):
    return get_scale_fretboard(
        root=request.root,
        scale=request.scale,
        notes=request.notes,
    )