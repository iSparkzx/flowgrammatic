import json
import sys
import os
import base64
import urllib.request
import urllib.error

API_KEY = os.environ.get("GOOGLE_API_KEY")
if not API_KEY:
    print("Error: GOOGLE_API_KEY environment variable not set")
    sys.exit(1)
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={API_KEY}"

prompt = """Create a horizontal inline logo for "Flowgrammatic" — an AI automation agency.

CRITICAL: TRANSPARENT background — NO background color at all. The image must have a transparent/clear background (PNG with alpha transparency).

LAYOUT: Icon on the LEFT, wordmark "Flowgrammatic" on the RIGHT, side by side on the same horizontal line.

Design specs:
- Logomark (left): Compact abstract geometric "F" made from 3-4 flowing gradient lines suggesting data streams. Small circular nodes at line endpoints.
- Gradient on icon: Electric blue (#0066FF) to bright cyan (#00D4FF)
- Wordmark (right): "Flowgrammatic" in clean, bold, modern white sans-serif typeface
- Horizontal composition
- Ultra minimal, premium, clean
- TRANSPARENT BACKGROUND — this is critical, no solid color behind it"""

payload = {
    "contents": [{
        "parts": [{"text": prompt}]
    }],
    "generationConfig": {
        "responseModalities": ["TEXT", "IMAGE"],
        "temperature": 0.8,
    }
}

headers = {"Content-Type": "application/json"}
data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(API_URL, data=data, headers=headers, method="POST")

try:
    print("Generating transparent logo...")
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    for candidate in result.get("candidates", []):
        content = candidate.get("content", {})
        for part in content.get("parts", []):
            if "inlineData" in part:
                img_data = base64.b64decode(part["inlineData"]["data"])
                output_path = "C:/Users/flowg/clawd/flowgrammatic/flowgrammatic-logo-clear.png"
                with open(output_path, "wb") as f:
                    f.write(img_data)
                print(f"Logo saved to: {output_path}")
                print(f"Size: {len(img_data)} bytes")
                sys.exit(0)
            elif "text" in part:
                print(f"Text: {part['text'][:200]}")

    print("No image generated")
    sys.exit(1)

except urllib.error.HTTPError as e:
    body = e.read().decode("utf-8", errors="replace")
    print(f"HTTP Error {e.code}: {body[:500]}")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
