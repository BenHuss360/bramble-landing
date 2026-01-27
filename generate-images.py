#!/usr/bin/env python3
"""Generate images for Bramble landing page using Imagen 4."""

import os, sys
from pathlib import Path
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    key_file = Path.home() / ".config" / "gemini" / "api_key"
    if key_file.exists():
        API_KEY = key_file.read_text().strip()
    else:
        sys.exit("Set GEMINI_API_KEY env var or put key in ~/.config/gemini/api_key")
client = genai.Client(api_key=API_KEY)
OUTPUT_DIR = Path("/root/clawd/bramble-landing/img")
OUTPUT_DIR.mkdir(exist_ok=True)

IMAGES = {
    "card-estate": {
        "prompt": (
            "Aerial photograph of a grand English country house surrounded by manicured gardens, "
            "parkland, and ancient woodland. Warm golden afternoon light. Rolling green Somerset hills "
            "in the background. The estate grounds stretch out with winding paths, a walled garden, "
            "and a lake glimpsed through trees. Premium, aspirational, peaceful. "
            "No people, no text, no UI. Professional drone photography, ultra high quality."
        ),
        "aspect_ratio": "16:9",
    },
    "card-wellness": {
        "prompt": (
            "Serene photograph of a wellness retreat nestled in English countryside. "
            "A timber and stone cabin or lodge surrounded by wildflower meadows and silver birch trees. "
            "Morning mist rising from the ground. Yoga deck or outdoor seating visible. "
            "Calming, grounded, nature-immersed. Digital detox atmosphere. "
            "No people, no text, no UI. Professional photography, soft natural light."
        ),
        "aspect_ratio": "16:9",
    },
    "card-garden": {
        "prompt": (
            "Photograph of a beautiful formal English garden at a historic house. "
            "Clipped box hedges, herbaceous borders in full bloom, a stone sundial or urn as focal point. "
            "Gravel paths leading between garden rooms. Cotswold stone walls in the background. "
            "Summer afternoon light. Classic, timeless, beautifully maintained. "
            "No people, no text, no UI. Professional garden photography."
        ),
        "aspect_ratio": "16:9",
    },
    "hero-bg": {
        "prompt": (
            "Dark, atmospheric aerial photograph of English woodland canopy at twilight. "
            "Deep forest greens fading to darkness at the edges. Subtle mist between the treetops. "
            "A single winding path barely visible through the canopy. Moody, mysterious, elegant. "
            "The colours should be deep forest green tones matching hex #052000. "
            "No people, no text, no UI. Professional drone photography, very dark and atmospheric."
        ),
        "aspect_ratio": "16:9",
    },
}

def generate(name, prompt, aspect_ratio="16:9"):
    print(f"\n🎨 Generating {name}...")
    try:
        response = client.models.generate_images(
            model="imagen-4.0-generate-001",
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio=aspect_ratio,
            ),
        )
        for img in response.generated_images:
            out_path = OUTPUT_DIR / f"{name}.png"
            out_path.write_bytes(img.image.image_bytes)
            print(f"   ✅ {out_path.name} ({len(img.image.image_bytes)//1024}KB)")
            return True
    except Exception as e:
        print(f"   ❌ {e}")
        return False

if __name__ == "__main__":
    targets = sys.argv[1:] if len(sys.argv) > 1 else list(IMAGES.keys())
    for name in targets:
        if name in IMAGES:
            cfg = IMAGES[name]
            generate(name, cfg["prompt"], cfg.get("aspect_ratio", "16:9"))
    print("\nDone!")
