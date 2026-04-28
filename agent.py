from storage import save_to_history, update_google_sheets
from vision import run_local_vision_agent


MODEL_NAME = "llama3.2-vision"
IMAGE_PATH = "images/cVsEvlhs.jpg"
CONTEXT_PATH = "aquarium_40_context.json"

# 3. Paleidimas
if __name__ == "__main__":
    ai_ataskaita = run_local_vision_agent(
        model=MODEL_NAME, image_path=IMAGE_PATH, context_path=CONTEXT_PATH
    )

    save_to_history(ai_ataskaita)
    update_google_sheets(ai_ataskaita)
