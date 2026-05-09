def direct_search(text: str, pattern: str) -> bool:
    """Простой посимвольный поиск подстроки без встроенного оператора in."""
    if not pattern:
        return True

    source = text.lower()
    target = pattern.lower()
    source_len = len(source)
    target_len = len(target)

    for start in range(source_len - target_len + 1):
        matched = True
        for offset in range(target_len):
            if source[start + offset] != target[offset]:
                matched = False
                break
        if matched:
            return True

    return False
