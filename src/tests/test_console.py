import pytest
from src.console import Console


class TestConsole:

    @pytest.fixture
    def console(self):
        return Console()

    def test_request_command(self, mocker):
        mocker.patch("builtins.input", return_value="test")

        console = Console()
        console.request_command()

        assert console.get_input_command() == "test"
