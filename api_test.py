from google import genai
from google.genai import types
import time

client = genai.Client(api_key="YOUR_API_KEY_HERE")

system_prompt = """
You are a customer support assistant for "TechStore", an electronics store.

Information you know:
- Return period: 30 days, original invoice required
- Shipping time: 2-5 business days
- Warranty: 2 years
- Working hours: 09:00-18:00 weekdays
- Phone: 0850 123 45 67

Rules:
- Only answer questions related to this store
- If you don't know something, say "Let me connect you to our customer service team"
- Keep answers short and clear
- Respond in the same language the customer uses
"""

history = []

print("TechStore Customer Support. How can I help you?\n")

while True:
    user_input = input("Customer: ")

    if user_input.lower() == "quit":
        break

    history.append({"role": "user", "parts": [{"text": user_input}]})

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=history,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.2
        )
    )

    bot_reply = response.text
    history.append({"role": "model", "parts": [{"text": bot_reply}]})

    print(f"TechStore Bot: {bot_reply}\n")
    time.sleep(5)