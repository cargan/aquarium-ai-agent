from storage import save_to_logs

from vision_grok import analyze_aquarium_with_groq
from download_photo import download_latest_photo_from_drive


# for local development
# MODEL_NAME = "llama3.2-vision"
# CONTEXT_PATH = "aquarium_40_context.json"

if __name__ == "__main__":
    image = download_latest_photo_from_drive()
    # image = "snapshot_0.jpg"
    print("IMAGE:", image)
    if image:
        result = analyze_aquarium_with_groq(f"snapshots/{image}")
        save_to_logs(result)
        print(result)
        # ai_ataskaita = run_local_vision_agent(
        #     model=MODEL_NAME, image_path=f"snapshots/{image}", context_path=CONTEXT_PATH
        # )

        # save_to_history(ai_ataskaita)
        # update_google_sheets(ai_ataskaita)
