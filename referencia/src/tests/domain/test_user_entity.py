import pytest
from uuid import uuid4
from domain.task.task_entity import Task
from domain.user.user_entity import User


class TestUser:

    # Teste para inicialização do usuário
    def test_user_initialization(self):
        user_id = uuid4()
        user_name = "Test User"
        user = User(id=user_id, name=user_name)

        assert user.id == user_id
        assert user.name == user_name
        assert user.tasks == []

    # Teste para validação do ID do usuário
    def test_user_id_validation(self):
        with pytest.raises(Exception, match="id must be an UUID"):
            User(id="invalid_id", name="Test User")

    # Teste para validação do nome do usuário
    def test_user_name_validation(self):
        user_id = uuid4()
        with pytest.raises(Exception, match="name is required"):
            User(id=user_id, name="")

    # Teste para adicionar tarefas ao usuário
    def test_collect_tasks(self):
        user = User(id=uuid4(), name="Test User")
        task1 = Task(
            id=uuid4(),
            user_id=user.id,
            title="Task 1",
            description="Description 1",
            completed=False,
        )
        task2 = Task(
            id=uuid4(),
            user_id=user.id,
            title="Task 2",
            description="Description 2",
            completed=True,
        )

        user.collect_tasks([task1, task2])
        assert len(user.tasks) == 2
        assert task1 in user.tasks
        assert task2 in user.tasks

    # Teste para contagem de tarefas pendentes
    def test_count_pending_tasks(self):
        user = User(id=uuid4(), name="Test User")
        task1 = Task(
            id=uuid4(),
            user_id=user.id,
            title="Task 1",
            description="Description 1",
            completed=False,
        )
        task2 = Task(
            id=uuid4(),
            user_id=user.id,
            title="Task 2",
            description="Description 2",
            completed=False,
        )
        task3 = Task(
            id=uuid4(),
            user_id=user.id,
            title="Task 3",
            description="Description 3",
            completed=False,
        )

        task1.mark_as_completed()
        user.collect_tasks([task1, task2, task3])
        pending_count = user.count_pending_tasks()
        assert pending_count == 2  # task1 está concluída; task2 e task3 estão pendentes

    # Teste para verificar a contagem de tarefas pendentes em uma lista vazia
    def test_count_pending_tasks_empty(self):
        user = User(id=uuid4(), name="Test User")
        assert user.count_pending_tasks() == 0  # Não há tarefas

    # Teste para tentar coletar uma lista vazia de tarefas
    def test_collect_empty_task_list(self):
        user = User(id=uuid4(), name="Test User")
        user.collect_tasks([])  # Adiciona uma lista vazia de tarefas
        assert len(user.tasks) == 0  # A lista de tarefas deve permanecer vazia

    # Teste para verificar se o método count_pending_tasks lida corretamente quando todas as tarefas estão concluídas
    def test_all_tasks_completed(self):
        user = User(id=uuid4(), name="Test User")
        task1 = Task(
            id=uuid4(),
            user_id=user.id,
            title="Task 1",
            description="Description 1",
            completed=True,
        )
        task2 = Task(
            id=uuid4(),
            user_id=user.id,
            title="Task 2",
            description="Description 2",
            completed=True,
        )

        user.collect_tasks([task1, task2])
        assert user.count_pending_tasks() == 0  # Ambas as tarefas estão concluídas

    # Teste para verificar se o método count_pending_tasks lida corretamente quando há apenas uma tarefa
    def test_single_pending_task(self):
        user = User(id=uuid4(), name="Test User")
        task = Task(
            id=uuid4(),
            user_id=user.id,
            title="Task 1",
            description="Description 1",
            completed=False,
        )

        user.collect_tasks([task])
        assert user.count_pending_tasks() == 1  # Apenas uma tarefa pendente
