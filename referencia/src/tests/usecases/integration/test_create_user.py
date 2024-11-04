from uuid import UUID, uuid4
from application.user.create_user import CreateUser, CreateUserRequest
from infra.user.in_memory_user_repository import InMemoryUserRepository


class TestCreateUser:

    def test_create_user_with_valid_data(self):
        repository = InMemoryUserRepository()
        use_case = CreateUser(repository=repository)
        request = CreateUserRequest(name="João")
        response = use_case.execute(request)

        assert response is not None
        assert isinstance(response.id, UUID)
        assert len(repository.users) == 1

        persisted_user = repository.users[0]

        assert persisted_user.id == response.id
        assert persisted_user.name == "João"
