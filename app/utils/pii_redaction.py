import re
from typing import Pattern

# Simple regexes (extend per your needs)
EMAIL: Pattern = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE: Pattern = re.compile(r"\b(?:\+?\d{1,3}[ -]?)?(?:\(?\d{3}\)?[ -]?)?\d{3}[ -]?\d{4}\b")
CREDIT_CARD: Pattern = re.compile(r"\b(?:\d[ -]*?){13,19}\b")
IPV4: Pattern = re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b")

def redact_text(
    text: str,
    redact_emails: bool = True,
    redact_phones: bool = True,
    redact_cards: bool = True,
    redact_ips: bool = True,
    replacement_map: dict[str, str] | None = None,
) -> str:
    \"\"\"Redact common PII using simple regexes.
    This is a best-effort baseline; tune for your domain.

    Args:
        text: Input string.
        redact_emails/phones/cards/ips: Toggles for each category.
        replacement_map: Optional mapping category->replacement token.
                         Defaults: email->[EMAIL], phone->[PHONE], card->[CARD], ip->[IP]

    Returns:
        Redacted string.
    \"\"\"
    repl = {
        "email": "[EMAIL]",
        "phone": "[PHONE]",
        "card": "[CARD]",
        "ip": "[IP]",
    }
    if replacement_map:
        repl.update(replacement_map)

    out = text
    if redact_emails:
        out = EMAIL.sub(repl["email"], out)
    if redact_phones:
        out = PHONE.sub(repl["phone"], out)
    if redact_cards:
        out = CREDIT_CARD.sub(repl["card"], out)
    if redact_ips:
        out = IPV4.sub(repl["ip"], out)
    return out
