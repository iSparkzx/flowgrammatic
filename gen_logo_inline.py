import json
import sys
import base64
import urllib.request
import urllib.error

API_KEY = "REDACTED_API_KEY"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={API_KEY}"

prompt = """Create a horizontal inline logo for "Flowgrammatic" — an AI automation agency.

CRITICAL LAYOUT: The icon and wordmark must be SIDE BY SIDE on the same line — the icon on the LEFT, the wordmark "Flowgrammatic" immediately to the RIGHT of it. NOT stacked vertically. This is a horizontal lockup.

Design specs:
- SOLID BLACK background (#000000)
- Logomark (left side): A small, compact abstract geometric "F" made from 3-4 flowing gradient lines suggesting data streams and automation. Small glowing circular nodes at line endpoints. Keep it square-proportioned and compact.
- Wordmark (right side): "Flowgrammatic" in clean, bold, modern sans-serif typeface in white, vertically centered with the icon
- Small gap between icon and wordmark
- Gradient on icon: Electric blue (#0066FF) to bright cyan (#00D4FF)
- Subtle glow on the icon lines
- Wide horizontal composition (landscape orientation, roughly 4:1 or 3:1 aspect ratio)
- Ultra minimal, premium, clean
- The icon and text should feel like one unified horizontal mark"""

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
    print("Generating inline logo...")
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    for candidate in result.get("candidates", []):
        content = candidate.get("content", {})
        for part in content.get("parts", []):
            if "inlineData" in part:
                img_data = base64.b64decode(part["inlineData"]["data"])
                output_path = "C:/Users/flowg/clawd/flowgrammatic/flowgrammatic-logo-inline.png"
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
