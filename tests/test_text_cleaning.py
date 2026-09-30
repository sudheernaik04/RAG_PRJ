from core.text_cleaner import clean_text


def test_clean_text_removes_repeated_blank_lines_and_control_chars():
    raw = "Hello\n\n\nworld\x00\x01   with spaced text\r\n"
    cleaned = clean_text(raw)

    assert "Hello" in cleaned
    assert "world" in cleaned
    assert "\x00" not in cleaned
    assert "\n\n" not in cleaned
