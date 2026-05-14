from storage import save_to_logs

from vision_grok import analyze_aquarium_with_groq
from download_photo import download_latest_photo_from_drive


# for local development
# MODEL_NAME = "llama3.2-vision"
# CONTEXT_PATH = "aquarium_40_context.json"
#
#
def convert_to_jpeg(image_path):
    import os
    from datetime import datetime
    from PIL import Image
    from pillow_heif import register_heif_opener

    file_extension = os.path.splitext(image_path)[1].lower()

    with Image.open(f"snapshots/{image_path}") as img:
        if file_extension == ".heic" or img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        img.thumbnail((1024, 1024))

        file_name = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
        file_path = os.path.join("snapshots", file_name)
        img.save(file_path, format="JPEG", quality=85)

        return file_path


if __name__ == "__main__":
    image = download_latest_photo_from_drive()
    print("IMAGE:", image)
    file_path = convert_to_jpeg(image)
    print("IMAGE Converted:", file_path)
    if file_path:
        result = analyze_aquarium_with_groq(file_path)
        save_to_logs(result)
        print(result)
        # ai_ataskaita = run_local_vision_agent(
        #     model=MODEL_NAME, image_path=f"snapshots/{image}", context_path=CONTEXT_PATH
        # )

        # save_to_history(ai_ataskaita)
        # update_google_sheets(ai_ataskaita)
