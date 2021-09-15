"""Declare auxiliary functions."""

import time


def time_ms() -> float:
    """Return current time in milliseconds."""
    return time.time() * 1000
