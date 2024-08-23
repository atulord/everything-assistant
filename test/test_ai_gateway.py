import pytest
from unittest.mock import patch, Mock
from ai_gateway import AIGateway
from tools import get_route


@pytest.fixture
def ai_gateway():
    aig = AIGateway(provider='claude',
                    system_prompt="You are a helpful assistant.")
    aig.messages.append({"role": "user", "content": "Hello"})
    return aig


def test_init(ai_gateway):
    assert ai_gateway.provider == 'claude'
    assert ai_gateway.system_prompt == "You are a helpful assistant."
    assert isinstance(ai_gateway.tools, list)
    assert len(ai_gateway.messages) == 1


def test_get_client(ai_gateway):
    assert ai_gateway.get_client() is not None


def test_generate_tools_schema(ai_gateway):
    def t_fn():
        pass
    tools_schema = ai_gateway._generate_tools_schema([t_fn])
    assert isinstance(tools_schema, list)
    assert len(tools_schema) == 1
    assert 'name' in tools_schema[0]
    assert 'description' in tools_schema[0]
    assert 'input_schema' in tools_schema[0]
