
import os
from dotenv import load_dotenv
from openai import OpenAI

# Find the .env file in the main project folder.
PROJECT_FOLDER = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
ENV_FILE = os.path.join(PROJECT_FOLDER, ".env")

load_dotenv(ENV_FILE)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def extract_with_ai(raw_text, previous_error=None):
    """Extract invoice information using OpenAI."""

    if not OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY is missing. "
            "Check the .env file in your project folder."
        )

    client = OpenAI(api_key=OPENAI_API_KEY)

    prompt = f"""
Extract invoice information from the text below.

Return only a JSON object with these fields:
- vendor_name
- invoice_number
- invoice_date (YYYY-MM-DD)
- currency (USD, EUR, or GBP)
- line_items (list of description, quantity, unit_price, line_total)
- subtotal
- tax_amount
- total_amount

Use numbers for quantity and amounts.
Do not add information that is not present.
If information is missing, use an empty string for text fields,
an empty list for line_items, and 0 for numeric fields.

Invoice text:
{raw_text}
"""

    if previous_error:
        prompt += f"""

Your previous extraction failed validation.
Please correct these errors:
{previous_error}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You extract invoice data accurately. "
                    "Return valid JSON only."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )

    import json

    content = response.choices[0].message.content

    if not content:
        raise ValueError("OpenAI returned an empty response.")

    return json.loads(content)
