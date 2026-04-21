from api.routes.focus import router


def test_focus_router_registered():
    assert router.prefix == "/focus"
