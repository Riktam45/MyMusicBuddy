from fastapi import APIRouter, Depends

from app.auth.dependencies import current_user
from app.auth.permissions import require_role

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.get("/dashboard")
def admin_dashboard(
    user=Depends(current_user),
):
    require_role(user, "admin")

    return {
        "message": "Welcome Admin!",
        "user": user.username,
    }