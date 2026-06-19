import pytest
from unittest.mock import AsyncMock, MagicMock

from titanic_m_learning.app.use_cases.jack_query_interactor import JackQueryInteractor
from titanic_m_learning.app.dtos.jack_dto import JackIntroduceQuery, JackIntroduceResult


@pytest.fixture
def mock_repository():
    repo = MagicMock()
    repo.introduce_myself = AsyncMock(
        return_value=JackIntroduceResult(id=9, name="Jack Dawson", message="안녕하세요, 잭입니다.")
    )
    return repo


@pytest.fixture
def interactor(mock_repository):
    return JackQueryInteractor(
        repository=mock_repository,
        lowe=MagicMock(),
        rose=MagicMock(),
    )


class TestIntroduceMyself:
    async def test_calls_repository_with_correct_query(self, interactor, mock_repository):
        query = JackIntroduceQuery(id=9, name="Jack Dawson")
        await interactor.introduce_myself(query)
        mock_repository.introduce_myself.assert_called_once_with(query)

    async def test_returns_repository_response(self, interactor):
        query = JackIntroduceQuery(id=9, name="Jack Dawson")
        response = await interactor.introduce_myself(query)
        assert response == JackIntroduceResult(id=9, name="Jack Dawson", message="안녕하세요, 잭입니다.")
