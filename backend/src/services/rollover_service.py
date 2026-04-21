from services.core import FocusService


def run_rollover_check(focus_service: FocusService):
    return focus_service.rollover_stop()
