"""Automated tests (Stage 13). Run: python -m pytest tests  (or: python tests/test_core.py)"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image

from core.comic import ComicError, build_comic, generate_captions, parse_captions
from views.library import matches

GOOD = '{"captions": ["a", "b", "c", "d"]}'


class FakeOpenAI:
    """Pretends to be the OpenAI client so tests need no internet or API key."""
    def __init__(self, replies):
        self.replies, self.calls = list(replies), 0
        self.chat = self
        self.completions = self

    def create(self, **kwargs):
        self.calls += 1
        reply = self.replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        msg = type("M", (), {"content": reply})
        return type("R", (), {"choices": [type("C", (), {"message": msg})]})


def test_parse_good():
    assert parse_captions(GOOD) == ["a", "b", "c", "d"]


def test_parse_bad():
    for bad in ["not json", '{"captions": ["only one"]}', '{"x": 1}', '{"captions": ["a","b","c",""]}']:
        try:
            parse_captions(bad)
            assert False, bad
        except ComicError:
            pass


def test_retry_once_then_succeed():
    fake = FakeOpenAI([TimeoutError(), GOOD])
    assert generate_captions(fake, "story", {}) == ["a", "b", "c", "d"]
    assert fake.calls == 2


def test_gives_up_after_one_retry():
    fake = FakeOpenAI([TimeoutError(), TimeoutError(), GOOD])
    try:
        generate_captions(fake, "story", {})
        assert False
    except ComicError as e:
        assert "try again" in str(e)
    assert fake.calls == 2  # never a third attempt


def test_comic_is_2x2_png_and_photo_untouched():
    buf = io.BytesIO()
    Image.new("RGB", (800, 600), "blue").save(buf, format="JPEG")
    original = buf.getvalue()
    png = build_comic(original, ["one", "two", "three", "four"], panel=200)
    img = Image.open(io.BytesIO(png))
    assert img.format == "PNG" and img.width > 400
    assert buf.getvalue() == original  # original bytes unchanged


def test_search():
    m = {"title": "Beach day", "people": "Grandma", "story": "We built sandcastles"}
    assert matches(m, "grandma beach")
    assert matches(m, "")
    assert not matches(m, "birthday")


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("PASS", name)
