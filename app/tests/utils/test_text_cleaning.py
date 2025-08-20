from app.utils.text_cleaning import clean_text

def test_clean_text_basic():
    s = "Check this out: https://example.com @user #CoolStuff"
    out = clean_text(s, strip_hashtags=True)
    assert "http" not in out and "@" not in out and "#" not in out
