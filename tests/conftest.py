import pytest
import xerion

@pytest.fixture
def db():
    return xerion.extensions.DataBase()
