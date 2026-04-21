from db.session import get_store


def test_get_store():
    store = get_store()
    assert store is not None
