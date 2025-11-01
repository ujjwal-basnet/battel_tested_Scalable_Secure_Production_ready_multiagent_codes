from typing import List, Tuple, Dict
import re
import uuid


# Try to import Presidio; gracefully fall back to regex-based detection when not installed.
_HAS_PRESIDIO = True
try:
    from presidio_analyzer import AnalyzerEngine
except Exception:
    _HAS_PRESIDIO = False


def analyze_pii(text: str, language: str = "en") -> List[dict]:
    """Detect PII and return a list of match dicts.

    If Presidio is available it will be used. Otherwise a lightweight regex fallback
    detects common patterns (emails, basic credit card patterns).
    Each match dict contains: entity_type, start, end, score, fragment
    """
    if _HAS_PRESIDIO:
        engine = AnalyzerEngine()
        entities = [
            "EMAIL_ADDRESS",
            "CREDIT_CARD",
            "PERSON",
            "LOCATION",
            "CRYPTO",
            "IBAN_CODE",
            "MEDICAL_LICENSE",
            "PHONE_NUMBER",
            "PASSWORD",
        ]
        results = engine.analyze(text=text, entities=entities, language=language)

        out = []
        for r in results:
            out.append({
                "entity_type": r.entity_type,
                "start": r.start,
                "end": r.end,
                "score": getattr(r, "score", 1.0),
                "fragment": text[r.start:r.end],
            })
        return out

    # Regex fallback
    out = []
    for m in re.finditer(r"[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}", text):
        out.append({
            "entity_type": "EMAIL_ADDRESS",
            "start": m.start(),
            "end": m.end(),
            "score": 0.9,
            "fragment": m.group(0),
        })

    for m in re.finditer(r"\b(?:\d[ -]*?){13,19}\b", text):
        out.append({
            "entity_type": "CREDIT_CARD",
            "start": m.start(),
            "end": m.end(),
            "score": 0.8,
            "fragment": m.group(0),
        })

    return out


def anonymize_with_placeholders(text: str, matches: List[dict]) -> Tuple[str, List[Tuple[str, str]]]:
    """Replace detected spans with unique placeholders and return mapping.

    Uses UUID-backed placeholders to avoid accidental collisions with user text. Replacements are
    performed from end to start to preserve indices.
    Returns: (sanitized_text, mapping) where mapping is list of (placeholder, original_value) in original order.
    """
    if not matches:
        return text, []

    matches_sorted = sorted(matches, key=lambda m: m["start"], reverse=True)

    mapping: List[Tuple[str, str]] = []
    sanitized = text

    for m in matches_sorted:
        placeholder = f"__PII_{m['entity_type']}_{uuid.uuid4().hex}__"
        start = m["start"]
        end = m["end"]
        original = sanitized[start:end]

        sanitized = sanitized[:start] + placeholder + sanitized[end:]
        mapping.append((placeholder, original))

    mapping.reverse()
    return sanitized, mapping


def restore_placeholders(text: str, mapping: List[Tuple[str, str]]) -> str:
    """Restore placeholders in text using the mapping list (placeholder, original).

    Replacement uses exact placeholder tokens, so simple str.replace is safe.
    """
    out = text
    for placeholder, original in mapping:
        out = out.replace(placeholder, original)
    return out


def replace_pii_with_tags_using_analyzer(text: str) -> str:
    """Detect PII entities and replace them with specific tags."""
    matches = analyze_pii(text)

    # Replace detected entities with tags based on their type
    for match in sorted(matches, key=lambda m: m['start'], reverse=True):
        entity_type = match['entity_type']
        start = match['start']
        end = match['end']
        tag = f"<{entity_type.lower()}>"
        text = text[:start] + tag + text[end:]

    return text


def restore_tags_to_original_text(text: str, mapping: List[Tuple[str, str]]) -> str:
    """Restore tags like <email_address>, <credit_card>, <location> back to their original text using the mapping."""
    for placeholder, original in mapping:
        text = text.replace(placeholder, original)
    return text


# Test the function
if __name__ == "__main__":
    test_text = "ujjwaal@gmail.com is my email, my credit card is 4111 1111 1111 1111, and I live in Nepal."
    result = replace_pii_with_tags_using_analyzer(test_text)
    print(result)

    # Example usage
    input_text = "<email_address> is my email, my credit card is <credit_card>, and I live in <location>."
    mapping = [
        ("<email_address>", "ujjwaal@gmail.com"),
        ("<credit_card>", "4111 1111 1111 1111"),
        ("<location>", "Nepal")
    ]
    restored_text = restore_tags_to_original_text(input_text, mapping)
    print(restored_text)