import os
import json
from datetime import datetime
import ollama
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# 1. Konfigūracija
# Naudojame lokalų modelį, kurį atsisiuntei per Ollama
MODEL_NAME = "llama3.2-vision"
IMAGE_PATH = "images/nJrFco4Y.jpg"

CONTEXT_PATH = "aquarium_40_context.json"

# 2. Funkcija Google Sheets atnaujinimui
def update_google_sheets(report):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        client = gspread.authorize(creds)
        
        # SVARBU: Lentelės pavadinimas turi sutapti su tavo sukurtu Google Sheets
        sheet = client.open("Aqua Duomenys").sheet1
        
        # Paruošiame eilutę
        row = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            report.get('vandens_skaidrumas', 'N/A'),
            report.get('augalų_būklė', 'N/A'),
            report.get('gyventojų_patikra', 'N/A'),
            report.get('pastebėtos_anomalijos', 'N/A'),
            report.get('rekomendacija', 'N/A')
        ]
        
        sheet.append_row(row)
        print("📊 Google Sheets atnaujinta!")
    except Exception as e:
        print(f"❌ Klaida su Google Sheets: {e.text}")


def save_to_history(new_data):
    history_file = 'aquarium_history.json'
    
    # Pridedame laiko žymą
    new_data['timestamp'] = datetime.now().isoformat()
    
    if os.path.exists(history_file):
        with open(history_file, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            data.append(new_data)
            f.seek(0)
            json.dump(data, f, indent=2, ensure_ascii=False)
    else:
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump([new_data], f, indent=2, ensure_ascii=False)
    
    print(f"📂 Duomenys sėkmingai išsaugoti į {history_file}")

    import gspread
from oauth2client.service_account import ServiceAccountCredentials


def update_google_sheets(ai_report):
    # Konfigūracija
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    
    # Atidaryk lentelę pagal pavadinimą
    sheet = client.open("Aqua Duomenys").sheet1
    
    # Paruošiame eilutę (ištraukiame duomenis iš AI JSON)
    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ai_report.get('vandens_skaidrumas', ''),
        ai_report.get('augalų_būklė', ''),
        ai_report.get('gyventojų_patikra', ''),
        ai_report.get('rekomendacija', '')
    ]
    
    sheet.append_row(row)
    print("📊 Google Sheets lentelė atnaujinta!")

# 2. Pagrindinė Agento funkcija
def run_local_vision_agent():
    print(f"📸 [Lokalus Vision Agent] Analizuoju nuotrauką {IMAGE_PATH} naudojant {MODEL_NAME}...")

    # A. Patikriname ar failai egzistuoja
    if not os.path.exists(IMAGE_PATH):
        print(f"❌ Klaida: Nerastas failas {IMAGE_PATH}")
        return

    if not os.path.exists(CONTEXT_PATH):
        print(f"❌ Klaida: Nerastas {CONTEXT_PATH} failas.")
        return

    # B. Nuskaitome kontekstą
    try:
        with open(CONTEXT_PATH, "r", encoding='utf-8') as f:
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
        model=MODEL_NAME,
        messages=[{
            'role': 'user',
            'content': system_prompt,
            'images': [IMAGE_PATH]
        }]
    )

    ai_response_text = response['message']['content'].strip()

    clean_json = ai_response_text[ai_response_text.find("{"):ai_response_text.rfind("}")+1]
    ai_ataskaita = json.loads(clean_json)
    print("\n✅ [AI Ataskaita] Sėkmingai sugeneruota lokaliai!")
    print(json.dumps(ai_ataskaita, indent=2, ensure_ascii=False))

    save_to_history(ai_ataskaita)
    update_google_sheets(ai_ataskaita)




# 3. Paleidimas
if __name__ == "__main__":
    run_local_vision_agent()
