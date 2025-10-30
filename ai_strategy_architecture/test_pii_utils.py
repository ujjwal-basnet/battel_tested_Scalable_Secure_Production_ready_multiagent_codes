from pii_utils import analyze_pii, anonymize_with_placeholders, restore_placeholders


def test_anonymize_and_restore_roundtrip():
    text = "Contact me at test.user@example.com or call 4111 1111 1111 1111. My name is Alice."

    matches = analyze_pii(text)
    assert isinstance(matches, list)

    sanitized, mapping = anonymize_with_placeholders(text, matches)
    # Ensure something changed if matches found
    if matches:
        assert sanitized != text
        # restore and confirm equality
        restored = restore_placeholders(sanitized, mapping)
        assert restored == text
    else:
        # no matches => sanitized should equal original
        assert sanitized == text
