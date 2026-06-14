#!/usr/bin/env python3
"""
Auto-generate a preview website for a local business using Claude.
"""

import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

import anthropic

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an expert web designer. Generate a complete, beautiful single-page HTML website
for a local business. The site should look professional and modern — clean layout, good fonts (use Google Fonts),
a hero section, services section, and a contact section with their phone number.
Use inline CSS only (no external CSS files). Make it mobile-friendly.
Output ONLY the raw HTML — no explanation, no markdown, no code blocks."""


def generate_website(business: dict) -> str:
    prompt = f"""Create a professional website for this local business:

Business Name: {business['name']}
Type: {business['type'].replace('_', ' ').title()}
Address: {business['address']}
Phone: {business['phone']}
Rating: {business.get('rating', 'N/A')} stars

Make it look like a real, high-quality local business site. Include:
- Eye-catching hero with the business name and a tagline
- A services section (infer 4-6 likely services from the business type)
- A "Why Choose Us" section
- Contact info and a call-to-action button that calls their number
- Professional color scheme that fits the business type"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
        system=SYSTEM_PROMPT,
    )

    html = message.content[0].text.strip()
    # Strip markdown code fences if model adds them
    html = re.sub(r"^```html?\n?", "", html)
    html = re.sub(r"\n?```$", "", html)
    return html


def deploy_to_vercel(html: str, business_name: str) -> str:
    """Deploy HTML to Vercel and return the live URL."""
    token = os.getenv("VERCEL_TOKEN")
    if not token:
        raise ValueError("VERCEL_TOKEN not set")

    slug = re.sub(r"[^a-z0-9]", "-", business_name.lower())[:40]

    with tempfile.TemporaryDirectory() as tmpdir:
        site_dir = Path(tmpdir) / "site"
        site_dir.mkdir()
        (site_dir / "index.html").write_text(html)

        result = subprocess.run(
            ["vercel", "--prod", "--yes", "--token", token, str(site_dir)],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(f"Vercel deploy failed: {result.stderr}")

        # Extract URL from output
        for line in result.stdout.splitlines():
            if line.startswith("https://"):
                return line.strip()

        raise RuntimeError("Could not find deployment URL in Vercel output")


def build_and_deploy(business: dict, output_dir: Path = Path("sites")) -> str:
    output_dir.mkdir(exist_ok=True)
    slug = re.sub(r"[^a-z0-9]", "-", business["name"].lower())[:40]
    html_file = output_dir / f"{slug}.html"

    print(f"  Generating website for {business['name']}...")
    html = generate_website(business)
    html_file.write_text(html)
    print(f"  Saved HTML → {html_file}")

    print(f"  Deploying to Vercel...")
    url = deploy_to_vercel(html, business["name"])
    print(f"  Live at: {url}")
    return url


if __name__ == "__main__":
    # Test with a single fake business
    test_biz = {
        "name": "KC Fresh Cuts",
        "type": "barbershop",
        "address": "1234 Main St, Kansas City, MO",
        "phone": "(816) 555-0123",
        "rating": 4.5,
    }
    url = build_and_deploy(test_biz)
    print(f"\nPreview URL: {url}")
