from fastapi import APIRouter, HTTPException
from infra.user.in_memory_user_repository import InMemoryUserRepository
from application.user.create_user import CreateUser, CreateUserRequest
from application.user.find_user import FindUser, FindUserRequest
from uuid import UUID

router = APIRouter(prefix="/users", tags=["Users"])

repository = InMemoryUserRepository()


@router.post("/")
def create_user(request: CreateUserRequest):
    try:
        usecase = CreateUser(repository)
        output = usecase.execute(request)
        return output

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{user_id}")
def find_user(
    user_id: UUID,
):
    try:
        usecase = FindUser(repository)
        output = usecase.execute(FindUserRequest(id=user_id))
        return output

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
