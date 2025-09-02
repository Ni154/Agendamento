from fastapi import APIRouter, Depends
from middleware.auth import get_current_user
from schemas.user import UserOut

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/me", response_model=UserOut)
def me(user = Depends(get_current_user)):
    return UserOut(id=user.id, name=user.name, email=user.email, role=user.role)

