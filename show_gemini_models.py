from utils import load_config
_config = load_config()
from google import genai

gemini_key = _config.get("tokens", "gemini_api_key", fallback=None)
client = genai.Client(api_key=gemini_key)


print(f"{'MODEL ID':<40} | {'DISPLAY NAME'}")
print("-" * 70)

try:
    # In the 2026 SDK, list() returns an iterator of Model objects
    for m in client.models.list():
        # m.name usually looks like 'models/gemini-2.0-flash'
        # m.display_name is the friendly name
        print(f"{m.name:<40} | {m.display_name}")
except Exception as e:
    print(f"Error: {e}")

