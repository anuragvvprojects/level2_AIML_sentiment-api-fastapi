import re
import unicodedata
from typing import Dict

# Minimal demojize map to avoid external deps. Extend as needed.
_DEFAULT_MAP: Dict[str, str] = {
    "😀": ":grinning_face:",
    "😁": ":beaming_face_with_smiling_eyes:",
    "😂": ":face_with_tears_of_joy:",
    "😊": ":smiling_face_with_smiling_eyes:",
    "😍": ":smiling_face_with_heart_eyes:",
    "🤔": ":thinking_face:",
    "👍": ":thumbs_up:",
    "👎": ":thumbs_down:",
    "🔥": ":fire:",
    "💯": ":hundred_points:",
    "❤️": ":red_heart:",
    "💔": ":broken_heart:",
    "🙏": ":folded_hands:",
    "👏": ":clapping_hands:",
    "😢": ":crying_face:",
    "😭": ":loudly_crying_face:",
    "😡": ":pouting_face:",
    "😠": ":angry_face:",
    "😎": ":smiling_face_with_sunglasses:",
    "🙂": ":slightly_smiling_face:",
    "🙃": ":upside_down_face:",
}

# Variation selectors & skin tone modifiers (basic handling)
VS16 = "\\uFE0F"
SKIN_TONE_MODIFIERS = "[\\U0001F3FB-\\U0001F3FF]"

def _strip_variations(s: str) -> str:
    s = re.sub(VS16, "", s)
    s = re.sub(SKIN_TONE_MODIFIERS, "", s)
    return s

def normalize_emojis(text: str, mapping: Dict[str, str] | None = None) -> str:
    \"\"\"Normalize emojis by removing variation selectors and mapping to :shortcodes:.
    If a character is not found in the mapping, keep it as-is.

    Args:
        text: Input text that may contain emoji.
        mapping: Optional override mapping of emoji->shortcode.

    Returns:
        Normalized string with mapped shortcodes for known emoji.
    \"\"\"
    mapping = mapping or _DEFAULT_MAP
    text = unicodedata.normalize("NFC", text)
    text = _strip_variations(text)

    # Replace mapped emoji codepoints with shortcodes.
    # This naive pass iterates known keys for simplicity.
    out = []
    for ch in text:
        out.append(mapping.get(ch, ch))
    return "".join(out)
