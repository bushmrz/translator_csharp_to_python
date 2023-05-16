from typing import Callable, Any

report_error: Callable[[int, str], None] = None
runtime_error: Callable[[Any, str], None] = None
scanner_error: Callable[[int, str], None] = None
init_language: Callable[[Callable[[int, str], None], Callable[[Any, str], None]], None] = None
