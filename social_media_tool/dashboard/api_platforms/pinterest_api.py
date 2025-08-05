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
        "title": "Pin from Base64 Image",
        "description": text,
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
    # 4. Handle result
    if res.status_code == 201:
        pin = res.json()
        print(f"✅ Pin created! ID: {pin['id']} | URL: https://pin.it/{pin['id']}")
    else:
        print("Pin creation failed")
        print("Status:", res.status_code)
        print("Response:", res.json())

#example usage. can be deleted after connecting to frontend
post_pin("new pin", "temp/image.jpg")

