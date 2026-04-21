from api.routes import tasks, focus, timeline


def test_routes_have_router_objects():
    assert tasks.router is not None
    assert focus.router is not None
    assert timeline.router is not None
