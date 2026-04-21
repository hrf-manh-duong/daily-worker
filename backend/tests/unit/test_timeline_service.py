from api.dependencies import timeline_service


def test_timeline_returns_list():
    events = timeline_service.today()
    assert isinstance(events, list)
