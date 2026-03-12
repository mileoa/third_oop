import pytest
from src.player import Player


class TestPlayer:

    @pytest.fixture
    def player(self):
        return Player()

    def test_player_init(self, player):
        assert player.get_available_bonuses() == []

    def test_add_bonus(self, player):
        player.add_bounus("test")
        assert player.get_available_bonuses() == ["test"]

    def test_remove_bonus_ok(self, player):
        player.add_bounus("test")

        player.remove_bounus("test")

        assert player.get_available_bonuses() == []
        assert player.get_remove_bonus_status() == player.REMOVE_BONUS_OK

    def test_remove_bonus_not_exists(self, player):
        player.add_bounus("test")

        player.remove_bounus("another_test")

        assert player.get_available_bonuses() == ["test"]
        assert player.get_remove_bonus_status() == player.REMOVE_BONUS_ERR_NOT_EXISTS

    def test_has_bonus_ok(self, player):
        player.add_bounus("test")

        assert player.has_bonus("test")

    def test_has_bonus_empty(self, player):
        assert not player.has_bonus("test")

    def test_has_bonus_not_existst(self, player):
        player.add_bounus("test1")

        assert not self.player.has_bonus("test")

    def test_clear(self, player):
        player.add_bounus("test")

        player.clear()

        assert player.get_available_bonuses() == []
