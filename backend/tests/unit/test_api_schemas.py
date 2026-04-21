from api.schemas import CreateTaskRequest


def test_schema_title_validation():
    model = CreateTaskRequest(title="abc")
    assert model.title == "abc"
