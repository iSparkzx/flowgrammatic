import json
import sys
import base64
import urllib.request
import urllib.error

API_KEY = "REDACTED_API_KEY"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={API_KEY}"

prompt = """Design a clean, modern, minimal logo for "Flowgrammatic" — an AI automation agency.

Requirements:
- The logo should be an icon/logomark + wordmark combination
- Icon concept: abstract flowing data streams or connected nodes forming an "F" shape, suggesting flow and automation
- Clean geometric lines, modern tech aesthetic
- Color scheme: electric blue (#0066FF) transitioning to cyan (#00D4FF) as a gradient
- The wordmark "Flowgrammatic" should use a clean, bold sans-serif font
- Dark background (#050510) so the logo pops
- Professional, premium feel — think top-tier SaaS company
- No busy details — clean and scalable
- The icon should work standalone as an app icon
- Output as a centered logo on the dark background
- Make it look like it was designed by a world-class brand agency"""

payload = {
    "contents": [{
        "parts": [{"text": prompt}]
    }],
    "generationConfig": {
        "responseModalities": ["TEXT", "IMAGE"],
        "temperature": 1.0,
    }
}

headers = {"Content-Type": "application/json"}
data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(API_URL, data=data, headers=headers, method="POST")

try:
    print("Generating logo...")
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    # Extract image from response
    for candidate in result.get("candidates", []):
        content = candidate.get("content", {})
        for part in content.get("parts", []):
            if "inlineData" in part:
                img_data = base64.b64decode(part["inlineData"]["data"])
                output_path = "C:/Users/flowg/clawd/flowgrammatic/flowgrammatic-logo.png"
                with open(output_path, "wb") as f:
                    f.write(img_data)
                print(f"Logo saved to: {output_path}")
                print(f"Size: {len(img_data)} bytes")
                sys.exit(0)
            elif "text" in part:
                print(f"Text response: {part['text'][:200]}")

    print("No image generated in response")
    print(json.dumps(result, indent=2)[:1000])
    sys.exit(1)

except urllib.error.HTTPError as e:
    body = e.read().decode("utf-8", errors="replace")
    print(f"HTTP Error {e.code}: {body[:500]}")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
