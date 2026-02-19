import copy

import pytest

import src.app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities dict before/after each test (preserves object identity)."""
    orig = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(orig)
