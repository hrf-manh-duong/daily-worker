from api.routes.timeline import router


def test_timeline_router_registered():
    assert router.prefix == "/timeline"
