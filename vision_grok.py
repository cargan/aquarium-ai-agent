import os
import json
import requests
import base64
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

import io
import base64
import os
from PIL import Image
from pillow_heif import register_heif_opener

# Įgaliname HEIC palaikymą Pillow bibliotekoje
register_heif_opener()


def get_base64_from_file(file_path):
    with open(file_path, "rb") as image_file:
        # Nuskaitome baitus ir koduojame
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        return encoded_string


def analyze_aquarium_with_groq(image_path):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        print("❌ Klaida: GROQ_API_KEY nerastas aplinkos kintamuosiuose.")
        return None

    try:
        base64_image = get_base64_from_file(image_path)

        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "meta-llama/llama-4-scout-17b-16e-instruct",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analyze this aquarium. Return JSON with keys: analysis, metrics (fish_count, water_clarity).",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.1,
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            result_content = response.json()["choices"][0]["message"]["content"]
            result = json.loads(result_content)  # Konvertuojame JSON stringą į dict

            result["date"] = datetime.now().isoformat()  # Pridedame datą prie rezultato
            result["image_filename"] = image_path.split("/")[
                -1
            ]  # Pridedame nuotraukos pavadinimą prie rezultato
            return json.dumps(result, ensure_ascii=False, indent=4)
        else:
            # Išspausdiname tikslią žinutę iš Groq serverio
            print(f"❌ Groq klaida 400! Detalės: {response.text}")
            return None

    except Exception as e:
        print(f"❌ Kritinė klaida: {e}")
        return None
