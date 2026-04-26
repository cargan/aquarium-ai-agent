import os
import json

import ollama


def run_local_vision_agent(model, image_path, context_path):
    print(
        f"📸 [Lokalus Vision Agent] Analizuoju nuotrauką {image_path} naudojant {model}..."
    )

    # A. Patikriname ar failai egzistuoja
    if not os.path.exists(image_path):
        print(f"❌ Klaida: Nerastas failas {IMAGE_PATH}")
        return

    if not os.path.exists(context_path):
        print(f"❌ Klaida: Nerastas {context_path} failas.")
        return

    # B. Nuskaitome kontekstą
    try:
        with open(context_path, "r", encoding="utf-8") as f:
            aquarium_context = json.load(f)
    except Exception as e:
        print(f"❌ Klaida nuskaitant kontekstą: {e}")
        return

    # C. Suformuojame griežtą instrukciją (System Prompt)
    system_prompt = f"""
    Aš esu profesionalus akvariumų analizės AI. Turiu analizuoti pateiktą nuotrauką,
    remdamasis šiuo kontekstu: {json.dumps(aquarium_context, ensure_ascii=False)}.

    Mano tikslas - pastebėti bet kokius nukrypimus nuo normos ar sveikatos problemas.
    Atsakyti privalau TIKLIU JSON formatu (be jokio papildomo teksto ar paaiškinimų).
    Atsakymas turi prasidėti '{{' ir baigtis '}}'.

    JSON struktūra (lietuvių kalba):
    {{
      "vandens_skaidrumas": "Skaidrus/Debesuotas/Žalias",
      "dumbliai": "Ar matosi naujų dumblių rūšių? (Aprašyk)",
      "augalų_būklė": "Ar augalai atrodo žali ir sveiki? Ar matosi geltonų lapų ar skylių?",
      "gyventojų_patikra": "Ar matosi žuvys? Ar jos atrodo aktyvios? Kiek pavyko suskaičiuoti?",
      "pastebėtos_anomalijos": "Bet kokios kitos pastebėtos problemos (pvz., nešvarus stiklas, etc.)",
      "rekomendacija": "Ką daryti dabar? (Atsakyk vienu sakiniu)"
    }}
    """

    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": system_prompt, "images": [image_path]}],
    )

    ai_response_text = response["message"]["content"].strip()

    clean_json = ai_response_text[
        ai_response_text.find("{") : ai_response_text.rfind("}") + 1
    ]
    ai_ataskaita = json.loads(clean_json)
    print("\n✅ [AI Ataskaita] Sėkmingai sugeneruota lokaliai!")
    print(json.dumps(ai_ataskaita, indent=2, ensure_ascii=False))

    return ai_ataskaita
