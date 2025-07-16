def format_progress_bar(percent: int) -> str:
    filled_blocks = int(percent / 10)
    empty_blocks = 10 - filled_blocks
    return "▓" * filled_blocks + "░" * empty_blocks