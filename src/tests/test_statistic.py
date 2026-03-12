import pytest
from src.statistic import Statistic


class TestPlayingFieldATD:

    @pytest.fixture
    def statistic(self):
        return Statistic()

    def test_statistic_init(self, statistic):
        assert statistic.get_move_count() == 0
        assert statistic.get_score() == 0

    def test_record_move(self, statistic):
        score = 0
        for i in range(4):
            score += (i + 1) * 10

            statistic.record_move(1, 1, (i + 1) * 10)
            assert statistic.get_move_count() == i + 1
            assert statistic.get_score() == score

    def test_clear(self, statistic):
        for i in range(4):
            statistic.record_move(1, 1, i)

        statistic.clear()

        assert statistic.get_move_count() == 0
        assert statistic.get_score() == 0
