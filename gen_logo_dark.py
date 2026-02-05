import json
import sys
import base64
import urllib.request
import urllib.error

API_KEY = "REDACTED_API_KEY"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={API_KEY}"

prompt = """Create a sleek, premium logo on a SOLID BLACK background (#000000) for "Flowgrammatic" — an AI automation agency.

Design specs:
- Logomark: An abstract geometric "F" made from flowing gradient lines that suggest data streams and automation pipelines. Use 3-4 clean parallel lines that curve to form the F letterform, with small glowing circular nodes at the endpoints.
- Gradient: Electric blue (#0066FF) to bright cyan (#00D4FF) on the flowing lines
- The lines should have a subtle glow/luminosity effect against the black background
- Below the icon, the wordmark "Flowgrammatic" in a clean, modern, bold sans-serif typeface in white
- SOLID BLACK background, nothing else
- Centered composition
- Ultra clean, minimal, no unnecessary elements
- This should look like a $50,000 brand identity from Pentagram or Landor
- The icon should be simple enough to work as a favicon or app icon"""

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
    print("Generating dark logo...")
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    for candidate in result.get("candidates", []):
        content = candidate.get("content", {})
        for part in content.get("parts", []):
            if "inlineData" in part:
                img_data = base64.b64decode(part["inlineData"]["data"])
                output_path = "C:/Users/flowg/clawd/flowgrammatic/flowgrammatic-logo-dark.png"
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
