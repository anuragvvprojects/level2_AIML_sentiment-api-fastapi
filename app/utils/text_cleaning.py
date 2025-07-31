import html
import re
import unicodedata
from typing import Iterable

URL_RE   = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
MENTION  = re.compile(r"@\w+")
HASHTAG  = re.compile(r"#\w+")
MULTISPC = re.compile(r"\s+")

def _strip_control_chars(s: str) -> str:
    return "".join(ch for ch in s if unicodedata.category(ch)[0] != "C" or ch in ("\n", "\t"))

def clean_text(
    text: str,
    lowercase: bool = True,
    strip_urls: bool = True,
    strip_handles: bool = True,
    strip_hashtags: bool = False,
    collapse_whitespace: bool = True,
    unescape_html: bool = True,
) -> str:
    \"\"\"General-purpose text cleanup for sentiment inputs.

    Steps (configurable):
      - HTML entity unescape
      - Remove URLs, @mentions, and optional #hashtags
      - Normalize unicode (NFC) and strip control chars
      - Lowercase
      - Collapse whitespace

    Returns:
      Cleaned string.
    \"\"\"
    s = text or ""
    if unescape_html:
        s = html.unescape(s)
    if strip_urls:
        s = URL_RE.sub("", s)
    if strip_handles:
        s = MENTION.sub("", s)
    if strip_hashtags:
        s = HASHTAG.sub("", s)
    s = unicodedata.normalize("NFC", s)
    s = _strip_control_chars(s)
    if lowercase:
        s = s.lower()
    if collapse_whitespace:
        s = MULTISPC.sub(" ", s).strip()
    return s
