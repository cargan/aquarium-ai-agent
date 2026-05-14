import os
import requests
import base64

from dotenv import load_dotenv

load_dotenv()

import io
import base64
import os
from PIL import Image
from pillow_heif import register_heif_opener

# Įgaliname HEIC palaikymą Pillow bibliotekoje
register_heif_opener()


def get_processed_base64(image_path):
    """
    Pagrindinis metodas: nusprendžia, ar reikia konvertuoti,
    ir grąžina paruoštą Base64 eilutę.
    """
    file_extension = os.path.splitext(image_path)[1].lower()

    # 1. Atidarome nuotrauką (Pillow dėka HEIC atidaromas taip pat kaip JPEG)
    with Image.open(image_path) as img:
        # 2. Jei tai HEIC arba turi skaidrumo (PNG), konvertuojame į RGB
        if file_extension == ".heic" or img.mode in ("RGBA", "P"):
            img = convert_to_jpeg_format(img)

        # 3. Atliekame bendrą apdorojimą (resize, kokybė, base64)
        return finalize_image_for_api(img)


def convert_to_jpeg_format(img_obj):
    """
    Metodas, atsakingas tik už spalvų erdvės sutvarkymą.
    """
    return img_obj.convert("RGB")


def finalize_image_for_api(img_obj, max_size=(1024, 1024)):
    """
    Metodas, atsakingas už rezoliucijos mažinimą ir kodavimą.
    """
    # Proporcingai sumažiname nuotrauką, kad neviršytų limitų
    img_obj.thumbnail(max_size)

    # Išsaugome į buferį
    buffer = io.BytesIO()
    img_obj.save(buffer, format="JPEG", quality=85)

    # Paverčiame į Base64
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def analyze_aquarium_with_groq(image_path):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        print("❌ Klaida: GROQ_API_KEY nerastas aplinkos kintamuosiuose.")
        return None

    try:
        base64_image = get_processed_base64(image_path)

        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            # "model": "llama-3.1-8b-instant",
            # "model": "llama-3.2-11b-vision-preview",
            "model": "meta-llama/llama-4-scout-17b-16e-instruct",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analyze this aquarium. Return JSON with keys: date, analysis, metrics (fish_count, water_clarity).",
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
            return response.json()["choices"][0]["message"]["content"]
        else:
            # Išspausdiname tikslią žinutę iš Groq serverio
            print(f"❌ Groq klaida 400! Detalės: {response.text}")
            return None

    except Exception as e:
        print(f"❌ Kritinė klaida: {e}")
        return None
