from services.rollover_service import run_rollover_check
from api.dependencies import focus_service


def test_rollover_no_crash():
    result = run_rollover_check(focus_service)
    assert result is None or result.state in {"ended", "active"}
