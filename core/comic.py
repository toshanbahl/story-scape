"""AI captions (GPT-4o) and the four-panel comic image (Pillow). Stage 7."""
import io
import json
import textwrap

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

TIMEOUT_SECONDS = 30
ATTEMPTS = 2  # first try + one retry

PROMPT = """You turn a family memory into a four-panel comic.
Write exactly four short captions (max 20 words each) that tell the story in order:
1 setting the scene, 2 what happened, 3 the key moment, 4 how it ended or why it matters.
Use only facts from the story. Reply as JSON: {"captions": ["...", "...", "...", "..."]}"""


class ComicError(Exception):
    """Raised when captions cannot be generated; the message is safe to show the user."""


def parse_captions(text):
    """Turn the AI's JSON reply into a list of exactly four captions, or raise ComicError."""
    try:
        captions = json.loads(text)["captions"]
    except (ValueError, KeyError, TypeError):
        raise ComicError("The AI reply was not in the expected format.")
    if not isinstance(captions, list) or len(captions) != 4 or not all(isinstance(c, str) and c.strip() for c in captions):
        raise ComicError("The AI did not return four captions.")
    return [c.strip() for c in captions]


def generate_captions(client, story, details, model="gpt-4o"):
    """Ask the AI model for four captions. 30s timeout, one retry, then a friendly error."""
    user_msg = f"Details: {details}\n\nStory: {story}"
    last_error = None
    for _ in range(ATTEMPTS):
        try:
            reply = client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": PROMPT}, {"role": "user", "content": user_msg}],
                response_format={"type": "json_object"},
                timeout=TIMEOUT_SECONDS,
            )
            return parse_captions(reply.choices[0].message.content)
        except Exception as e:  # timeout, network, bad format: all get one retry
            last_error = e
    raise ComicError(f"Sorry, the comic could not be created right now. Please try again. ({type(last_error).__name__})")


def _panel(photo, index, size):
    """Make one comic-style panel. Each panel frames the photo differently."""
    w, h = photo.size
    crops = [
        (0, 0, w, h),                               # 1 whole scene
        (0, 0, w * 2 // 3, h),                      # 2 left side
        (w // 6, h // 6, w * 5 // 6, h * 5 // 6),   # 3 close-up on the middle
        (w // 3, 0, w, h),                          # 4 right side
    ]
    img = ImageOps.fit(photo.crop(crops[index]), size)
    img = ImageOps.posterize(img, 4).filter(ImageFilter.EDGE_ENHANCE_MORE)  # flat "comic" colours
    return img


def build_comic(photo_bytes, captions, panel=480):
    """Return PNG bytes of a 2x2 comic: each panel = photo framing + caption strip."""
    photo = ImageOps.exif_transpose(Image.open(io.BytesIO(photo_bytes))).convert("RGB")
    caption_h, gap = 110, 16
    sheet = Image.new("RGB", (gap + 2 * (panel + gap), gap + 2 * (panel + caption_h + gap)), "#FDF8F3")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default(size=20)

    for i, caption in enumerate(captions):
        x = gap + (i % 2) * (panel + gap)
        y = gap + (i // 2) * (panel + caption_h + gap)
        sheet.paste(_panel(photo, i, (panel, panel)), (x, y))
        draw.rectangle([x, y + panel, x + panel, y + panel + caption_h], fill="white")
        draw.rectangle([x, y, x + panel, y + panel + caption_h], outline="#2C1A0E", width=4)
        draw.text((x + 12, y + panel + 10), "\n".join(textwrap.wrap(caption, 40)[:4]), fill="#2C1A0E", font=font)

    out = io.BytesIO()
    sheet.save(out, format="PNG")
    return out.getvalue()
