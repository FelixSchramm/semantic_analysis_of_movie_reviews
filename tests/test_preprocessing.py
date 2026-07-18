from src.preprocessing import normalize_word, preprocess, unicode_to_ascii


def test_unicode_to_ascii_strips_accents():
    assert unicode_to_ascii("Café déjà vu") == "Cafe deja vu"


def test_preprocess_lowercases_and_filters():
    # Lower-cases, drops HTML, punctuation, digits, stop words and short tokens.
    tokens = preprocess("The CATS!! were running 12 times <br /> in Zürich.")
    assert tokens == ["cats", "running", "times", "zurich"]


def test_preprocess_removes_all_stopwords():
    assert preprocess("the and of a to") == []


def test_preprocess_drops_short_tokens():
    # "hi" (len 2) is below MIN_TOKEN_LEN and is dropped; "cat" (len 3) survives.
    assert preprocess("hi cat") == ["cat"]


def test_normalize_word_normalises_single_word():
    assert normalize_word("Running") == "running"


def test_normalize_word_returns_none_for_stopword():
    assert normalize_word("the") is None


def test_normalize_word_returns_none_for_empty():
    assert normalize_word("!!!") is None
