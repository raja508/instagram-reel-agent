import os
import time
from pathlib import Path
import mimetypes
from google import genai

import cloudinary
import cloudinary.uploader
import requests
from dotenv import dotenv_values, load_dotenv

# Load environment variables from this project's .env file
ENV_FILE = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=ENV_FILE, override=True)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

# Read Cloudinary configuration from .env
env_values = dotenv_values(ENV_FILE)
cloudinary_url = env_values.get("CLOUDINARY_URL", "").strip()

if cloudinary_url.startswith("cloudinary://"):
    credentials = cloudinary_url[len("cloudinary://"):]

    try:
        api_key, remaining = credentials.split(":", 1)
        api_secret, cloud_name = remaining.rsplit("@", 1)

        cloudinary.config(
            cloud_name=cloud_name.strip(),
            api_key=api_key.strip(),
            api_secret=api_secret.strip(),
            secure=True,
        )
    except ValueError:
        print("Invalid CLOUDINARY_URL format in .env")
else:
    print("CLOUDINARY_URL is missing or has an invalid format.")

IG_USER_ID = os.getenv("IG_USER_ID")
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")

API_VERSION = "v23.0"
BASE_URL = f"https://graph.instagram.com/{API_VERSION}"
VIDEO_FOLDER = Path(__file__).parent / "videos"

CAPTION = (
    "✨ Created with my Instagram Reel Posting Agent!\n"
    "🤖 Automating content, one Reel at a time.\n"
    "#InstagramReels #Automation #Python #AI"
)

def generate_caption(video_path):
    """Analyze the actual video and generate a relevant caption."""
    video_path = Path(video_path)

    print(f"Analyzing video with Gemini: {video_path.name}")

    try:
        uploaded_file = client.files.upload(file=str(video_path))

        while uploaded_file.state.name == "PROCESSING":
            time.sleep(2)
            uploaded_file = client.files.get(name=uploaded_file.name)

        if uploaded_file.state.name == "FAILED":
            raise RuntimeError("Gemini could not process the video.")

        prompt = """
        Analyze the actual video content.
        Identify what is shown, the topic, and the main message.
        Write a natural, engaging Instagram Reel caption in English.
        Add 5-8 relevant hashtags.
        Do not invent details that are not visible in the video.
        Return only the caption and hashtags.
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[uploaded_file, prompt],
        )

        caption = response.text.strip()
        print(f"Generated caption:\n{caption}")
        return caption

    except Exception as error:
        print(f"Video analysis failed: {error}")
        return (
            f"Watch this Reel! #InstagramReels #Reels"
        )

def upload_video(video_path):
    config = cloudinary.config()

    if not config.api_key or not config.api_secret or not config.cloud_name:
        raise RuntimeError(
            "Cloudinary configuration is incomplete. "
            "Check CLOUDINARY_URL in your .env file."
        )

    print(f"Uploading to Cloudinary: {video_path.name}")

    result = cloudinary.uploader.upload(
        str(video_path),
        resource_type="video",
    )

    video_url = result.get("secure_url")
    if not video_url:
        raise RuntimeError("Cloudinary did not return a secure video URL.")

    print("Cloudinary upload completed.")
    return video_url


def publish_reel(video_url, video_name):
    print(f"Creating Instagram Reel: {video_name}")

    response = requests.post(
        f"{BASE_URL}/{IG_USER_ID}/media",
        data={
            "media_type": "REELS",
            "video_url": video_url,
            "caption": generate_caption(VIDEO_FOLDER / video_name),
            "share_to_feed": "true",
            "access_token": META_ACCESS_TOKEN,
        },
        timeout=60,
    )

    if not response.ok:
        print("Container creation failed:", response.text)
        return False

    container_id = response.json().get("id")
    if not container_id:
        print("No container ID returned by Instagram.")
        return False

    for _ in range(36):
        result = requests.get(
            f"{BASE_URL}/{container_id}",
            params={
                "fields": "status_code",
                "access_token": META_ACCESS_TOKEN,
            },
            timeout=30,
        )

        if not result.ok:
            print("Status check failed:", result.text)
            return False

        status = result.json().get("status_code")
        print(f"{video_name} processing status: {status}")

        if status == "FINISHED":
            break

        if status == "ERROR":
            print("Instagram could not process this video.")
            return False

        time.sleep(5)
    else:
        print("Instagram processing timed out.")
        return False

    result = requests.post(
        f"{BASE_URL}/{IG_USER_ID}/media_publish",
        data={
            "creation_id": container_id,
            "access_token": META_ACCESS_TOKEN,
        },
        timeout=60,
    )

    if not result.ok:
        print("Publishing failed:", result.text)
        return False

    print("Published successfully:", video_name)
    print("Media ID:", result.json().get("id"))
    return True


def main():
    if not IG_USER_ID or not META_ACCESS_TOKEN:
        print("Check IG_USER_ID and META_ACCESS_TOKEN in .env")
        return

    if not cloudinary.config().api_key:
        print("Cloudinary API key was not loaded. Check .env.")
        return

    if not VIDEO_FOLDER.exists():
        print("Missing videos folder:", VIDEO_FOLDER)
        return

    videos = sorted(
        p for p in VIDEO_FOLDER.iterdir()
        if p.is_file() and p.suffix.lower() in (".mp4", ".mov")
    )

    if not videos:
        print("No MP4 or MOV videos found in the videos folder.")
        return

    print(f"Found {len(videos)} video(s):")
    for video in videos:
        print("-", video.name)

    print("\nWARNING: Each listed video will be published as a separate Instagram Reel.")
    confirm = input("Type POST to publish ALL listed videos: ")

    if confirm.strip() != "POST":
        print("Cancelled. Nothing was published.")
        return

    for video in videos:
        try:
            video_url = upload_video(video)
            publish_reel(video_url, video.name)
        except Exception as error:
            print(f"Failed for {video.name}: {error}")

        time.sleep(10)


if __name__ == "__main__":
    main()
