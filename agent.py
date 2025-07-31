import os
import time
import json
import google.generativeai as genai
from orgo import Computer

# --------------------------
# 🔐 API Keys & Setup
# --------------------------
os.environ["GOOGLE_API_KEY"] = "AIzaSyCn43FyMu0k4TpBrrXVo1KNRtPR1JuUoF4"
ORG_PROJECT_ID = "computer-p6yfozm"
ORG_API_KEY = "sk_live_ca47e2889d4239b7a253e357ab7bd0e532a81b66f20891f0"

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-pro-vision")

# --------------------------
# 🧠 Initialize Orgo Computer
# --------------------------
computer = Computer(project_id=ORG_PROJECT_ID, api_key=ORG_API_KEY)

# --------------------------
# 🧠 AI Product Extractor Function
# --------------------------
def extract_trending_products(name: str, url: str):
    print(f"\n🌐 Visiting: {name} - {url}")

    # Launch browser (first time only)
    computer.left_click(40, 40)  # Adjust to where Chrome icon is
    time.sleep(3)

    # Navigate to the category URL
    computer.type(url + "\n")
    time.sleep(8)

    # Scroll to load more items
    for _ in range(3):
        computer.scroll(0, 400)
        time.sleep(1)

    # Take screenshot
    image_path = f"{name.lower()}_screenshot.png"
    computer.screenshot(image_path)
    print(f"📸 Screenshot saved: {image_path}")

    # Load screenshot bytes
    with open(image_path, "rb") as img_file:
        image_bytes = img_file.read()

    # Gemini Prompt
    prompt = f"""
    From the screenshot of Amazon's {name} page, extract a list of the top trending products.
    For each product, extract:
    - Product name
    - Price
    - (Optional) Star rating if available
    Return results as JSON like:
    [
      {{"product": "...", "price": "...", "rating": "..."}}
    ]
    """

    # Send to Gemini Vision
    response = model.generate_content([
        prompt,
        {"mime_type": "image/png", "data": image_bytes}
    ])

    print(f"\n📦 Trending in {name}:\n")
    print(response.text)

    # Optional: Save output to JSON
    try:
        parsed_data = json.loads(response.text)
        with open(f"{name.lower()}_trending.json", "w", encoding="utf-8") as f:
            json.dump(parsed_data, f, indent=2)
        print(f"✅ Saved to {name.lower()}_trending.json")
    except Exception as e:
        print("⚠️ Could not parse Gemini output to JSON:", e)

# --------------------------
# 🔁 Trending Categories
# --------------------------
categories = {
    "Electronics": "https://www.amazon.in/gp/bestsellers/electronics",
    "Grocery": "https://www.amazon.in/s?i=grocery&bbn=2454178031&rh=n%3A2454178031&dc",
    "Fashion": "https://www.amazon.in/gp/bestsellers/fashion"
}

# --------------------------
# 🔁 Run For All Categories
# --------------------------
for category_name, category_url in categories.items():
    extract_trending_products(category_name, category_url)
