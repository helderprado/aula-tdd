from uuid import uuid4
from domain.user.user_entity import User
from infra.user.in_memory_user_repository import InMemoryUserRepository
from application.user.find_user import FindUser, FindUserRequest, FindUserResponse


class TestFindUser:

    def test_find_user_with_valid_data(self):

        user1 = User(id=uuid4(), name="João")
        user2 = User(id=uuid4(), name="Maria")
        repository = InMemoryUserRepository(users=[user1, user2])
        use_case = FindUser(repository=repository)
        request = FindUserRequest(id=user2.id)
        response = use_case.execute(request)

        assert response == FindUserResponse(id=user2.id, name=user2.name)
