import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

IG_USER_ID = os.getenv("IG_USER_ID")
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
VIDEO_URL = os.getenv("VIDEO_URL")

API_VERSION = "v23.0"
BASE_URL = f"https://graph.instagram.com/{API_VERSION}"


def main():
    if not IG_USER_ID or not META_ACCESS_TOKEN or not VIDEO_URL:
        print("Error: Check IG_USER_ID, META_ACCESS_TOKEN and VIDEO_URL in .env")
        return

    # Step 1: Create a Reel container
    print("Creating Instagram Reel container...")

    try:
        response = requests.post(
            f"{BASE_URL}/{IG_USER_ID}/media",
            data={
                "media_type": "REELS",
                "video_url": VIDEO_URL,
                "caption": "Posted using my Instagram Reel Posting Agent! #automation",
                "share_to_feed": "true",
                "access_token": META_ACCESS_TOKEN,
            },
            timeout=60,
        )

        if not response.ok:
            print("Container creation failed:", response.text)
            return

        container_id = response.json().get("id")

        if not container_id:
            print("Error: No container ID returned.")
            return

        # Step 2: Check video processing status
        print("Waiting for Instagram to process the video...")

        for attempt in range(24):
            status_response = requests.get(
                f"{BASE_URL}/{container_id}",
                params={
                    "fields": "status_code",
                    "access_token": META_ACCESS_TOKEN,
                },
                timeout=30,
            )

            if not status_response.ok:
                print("Status check failed:", status_response.text)
                return

            status = status_response.json().get("status_code")
            print(f"Processing status: {status}")

            if status == "FINISHED":
                break

            if status == "ERROR":
                print("Instagram reported a video-processing error.")
                return

            time.sleep(5)
        else:
            print("Video processing timed out. Please try again later.")
            return

        # Step 3: Publish the Reel
        print("Publishing Reel...")

        publish_response = requests.post(
            f"{BASE_URL}/{IG_USER_ID}/media_publish",
            data={
                "creation_id": container_id,
                "access_token": META_ACCESS_TOKEN,
            },
            timeout=60,
        )

        if not publish_response.ok:
            print("Publishing failed:", publish_response.text)
            return

        print("Reel published successfully!")
        print("Media ID:", publish_response.json().get("id"))

    except requests.RequestException as error:
        print("Network/API request failed:", error)


if __name__ == "__main__":
    main()