from app.utils.language_detect import detect_language

def test_detect_language_heuristics():
    assert detect_language("This is an English sentence.") in {"en","other"}
    assert detect_language("¿Dónde está la biblioteca?") in {"es","other"}
