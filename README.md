# Instagram Reel Posting Agent

A Python script that automatically publishes a video Reel to an Instagram Business account using the official Meta Graph API.

## Features

- Creates an Instagram Reel media container.
- Checks video processing status.
- Publishes the Reel automatically.
- Loads credentials securely from environment variables.

## Requirements

- Python 3.10 or newer
- Instagram Business account
- Meta access token with the required permissions
- Public HTTPS video URL

## Setup

1. Install the required packages:

   pip install requests python-dotenv

2. Create a `.env` file using `.env.example` as a template.

3. Add your Instagram User ID, Meta access token, and public video URL to `.env`.

4. Run the script:

   python reel_poster.py

## Security

Never share your Meta access token or upload the `.env` file to GitHub.

## Technologies

- Python
- Requests
- python-dotenv
- Meta Graph API