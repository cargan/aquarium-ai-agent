from storage import save_to_history, update_google_sheets
from vision import run_local_vision_agent
from download_photo import download_latest_photo_from_drive


MODEL_NAME = "llama3.2-vision"
CONTEXT_PATH = "aquarium_40_context.json"

if __name__ == "__main__":
    image = download_latest_photo_from_drive()
    if image:
        ai_ataskaita = run_local_vision_agent(
            model=MODEL_NAME, image_path=f"snapshots/{image}", context_path=CONTEXT_PATH
        )

        save_to_history(ai_ataskaita)
        update_google_sheets(ai_ataskaita)
