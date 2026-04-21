from api.routes.tasks import router


def test_tasks_router_registered():
    assert router.prefix == "/tasks"
