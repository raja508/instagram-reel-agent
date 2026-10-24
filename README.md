# 🚀 Instagram Reel Posting Agent

An AI-powered Python automation tool that publishes Instagram Reels using the official Meta Graph API, uploads videos to Cloudinary, and generates captions and hashtags using Google Gemini AI.

## ✨ Features

- 📹 **Automated Reel Publishing:** Publish videos to an Instagram Business account using the Meta Graph API.
- ☁️ **Cloudinary Integration:** Upload videos to Cloudinary to obtain publicly accessible video URLs.
- 🤖 **AI-Generated Captions:** Generate engaging captions and relevant hashtags using Google Gemini.
- 📂 **Multiple Video Support:** Process videos placed in a local `videos` folder.
- 🔐 **Environment Variable Security:** Store API credentials in a local `.env` file.
- ⚡ **Publishing Status Checks:** Check Instagram media processing status before publishing.
- 🛑 **Publishing Confirmation:** Confirm before publishing the listed videos.

## 🛠️ Tech Stack

- Python
- Instagram Graph API
- Google Gemini API
- Cloudinary
- Requests
- python-dotenv

## 📁 Project Structure

```text
instagram-reel-agent/
├── videos/
│   └── reel1.mp4
├── reel_poster.py
├── multi_reel_poster.py
├── multi_reel_poster_before_ai.py
├── .env.example
├── .gitignore
└── README.md
```

## ⚙️ Requirements

- Python 3.10 or later
- Instagram Business or Creator account
- Meta Graph API access and a valid access token
- Cloudinary account and API credentials
- Google Gemini API key

## 🚀 Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/raja508/instagram-reel-agent.git
cd instagram-reel-agent
```

### 2. Install dependencies

```bash
python -m pip install requests python-dotenv cloudinary google-genai
```

### 3. Configure environment variables

Create a local `.env` file in the project root using `.env.example` as a template.

Configure the required variables:

```env
IG_USER_ID=your_instagram_user_id
META_ACCESS_TOKEN=your_meta_access_token
CLOUDINARY_URL=cloudinary://your_api_key:your_api_secret@your_cloud_name
GEMINI_API_KEY=your_gemini_api_key
```

Replace the example values with your own credentials. Never commit your `.env` file or share your API keys and access tokens publicly.

### 4. Add videos

Place your MP4 or MOV video files inside the `videos` folder.

### 5. Run the application

For basic Reel publishing:

```bash
python reel_poster.py
```

For multi-video publishing with AI-generated captions:

```bash
python multi_reel_poster.py
```

Review the listed videos before confirming publication. Each confirmed video is processed and published as a separate Instagram Reel.

## 🔄 Workflow

1. Read video files from the local `videos` folder.
2. Upload each video to Cloudinary.
3. Generate a caption and hashtags using Gemini AI based on the video filename.
4. Create an Instagram Reel media container through the Meta Graph API.
5. Check the media processing status.
6. Publish the Reel after processing completes.

**Note:** Caption generation uses the filename to infer the video's topic; it does not currently analyze the actual video visuals.

## 🔒 Security

- Keep `.env` private and excluded from Git.
- Never hardcode API credentials in source code.
- Use `.env.example` to document required environment variables without real secrets.
- Rotate any credentials that have been exposed.

## 🎯 Project Objective

The objective of this project is to demonstrate social media automation using Python, AI-powered caption generation, cloud video hosting, and the official Instagram publishing API.

## 👨‍💻 Author

**Raja Kumar**

GitHub: https://github.com/raja508

---

*Built with Python, Google Gemini AI, Cloudinary, and the Instagram Graph API.*
