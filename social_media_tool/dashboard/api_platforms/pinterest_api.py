import os
import base64
import requests
from dotenv import load_dotenv


load_dotenv(dotenv_path="../../../.env")
ACCESS_TOKEN = os.getenv("PINTEREST_ACCESS_TOKEN")
print("ACCESS_TOKEN:", ACCESS_TOKEN)


# pinterest requires an image to create a pin. text-only posts are not possible
def post_pin(text, image_path):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    # 1. Get your boards
    res = requests.get(
        "https://api-sandbox.pinterest.com/v5/boards",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
    )
    print("Board API response:")
    print(res.status_code)
    print(res.json())
    boards = res.json().get("items", [])
    if not boards:
        print(" No boards found. Creating one...")
        res = requests.post(
            "https://api-sandbox.pinterest.com/v5/boards",
            headers=headers,
            json={
                "name": "My Test Sandbox Board",
                "description": "Created via API for sandbox testing"
            }
        )
        if res.status_code != 201:
            print("Failed to create board:", res.json())
            raise SystemExit
        print(res.json())
    board_id = boards[0]["id"]
    print(f"Using board: {board_id}")
    # 2. Read and encode image in base64
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    # 3. Create the Pin with image base64 data
    pin_payload = {
        "board_id": board_id,
        "title": text,
        "description": "Vortex Solution",
        "media_source": {
            "source_type": "image_base64",
            "content_type": "image/png",
            "data": encoded_string,
            "is_standard": True
        }
    }
    res = requests.post(
        "https://api-sandbox.pinterest.com/v5/pins",
        headers=headers,
        json=pin_payload
    )
    if res.status_code == 201:
        pin = res.json()
        pin_id = pin.get("id")
        url = f"https://pin.it/{pin_id}" if pin_id else None
        return True, pin_id, url

        # failure
    try:
        detail = res.json()
    except Exception:
        detail = res.text
    return False, None, f"Pin creation failed: {res.status_code} {detail}"



