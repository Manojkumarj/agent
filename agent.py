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
model = genai.GenerativeModel("gemini-2.0-flash")

# --------------------------
# 🧠 Initialize Orgo Computer
# --------------------------
computer = Computer(project_id=ORG_PROJECT_ID, api_key=ORG_API_KEY)

def extract_trending_products(name: str, url: str):
    print(f"\n🌐 Visiting: {name} - {url}")

    print("🦊 Launching Firefox browser...")
    computer.left_click(5, 5)
    computer.left_click(5, 150)
    time.sleep(10)  # Wait for browser to open

    # Step 2: Focus address bar and type URL
    print("⌨️ Typing URL...")
    computer.left_click(200, 60)
    time.sleep(1)

    # Type and go to the URL
    computer.type(url)
    time.sleep(0.5)
   
    computer.left_click(400, 200)  # 💡 Adjust as needed (somewhere in web content)
    time.sleep(10)

    # Step 4: Press Enter
    computer.type("[ENTER]")
    time.sleep(10)

    # Step 5: Scroll using arrow keys
    print("📜 Scrolling the page...")
    for _ in range(3):
        computer.type("[PAGE_DOWN]")
        time.sleep(1)
    # Step 4: Screenshot the page
    image_path = f"{name.lower()}_screenshot.png"
    image = computer.screenshot()  # Get the PIL Image object
    image.save(image_path) 
    print(f"📸 Screenshot saved: {image_path}")

    # Step 5: Send to Gemini
    with open(image_path, "rb") as img_file:
        image_bytes = img_file.read()

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

    print("🤖 Analyzing with Gemini...")
    response = model.generate_content([
        prompt,
        {"mime_type": "image/png", "data": image_bytes}
    ])

    print(f"\n📦 Trending in {name}:\n")
    print(response.text)

    # Save results
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
    "Electronics": "https://www.amazon.in/gp/bestsellers/electronics/ref=zg_bs_nav_electronics_0",
    "Grocery": "https://www.amazon.in/s?i=grocery&bbn=2454178031&rh=n%3A2454178031&dc",
    "Fashion": "https://www.amazon.in/gp/bestsellers/fashion"
}

# --------------------------
# 🔁 Run All
# --------------------------
for category_name, category_url in categories.items():
    extract_trending_products(category_name, category_url)
