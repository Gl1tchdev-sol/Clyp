# Clyp 🎥

**Clyp** is an AI-powered Twitter bot that transforms text prompts into short videos using Google’s cutting-edge Veo 3 video generation model. Just mention the bot on Twitter with a short description, and it will generate and reply to you with a custom-made 8-second video. ✨

---

## 🧠 Abstract

Clyp listens for mentions on Twitter and interprets any following text as a creative prompt. It then sends that prompt to Google's Vertex AI platform (Veo 3) to generate a video. Once the video is created and downloaded, the bot automatically replies to the original tweet with the video attached — making real-time, AI-generated multimedia content delivery as simple as tweeting a sentence.

---

## 🔧 How It Works

1. **Twitter Integration**
   - The bot authenticates using Twitter’s API.
   - It monitors mentions directed at its handle (e.g. `@Clyp`).

2. **Prompt Extraction**
   - When a tweet mentions the bot, it extracts the remaining text as a prompt.
   - Example: `@Clyp do a video of a dragon flying through a volcano` → `"do a video of a dragon flying through a volcano"`

3. **Video Generation with Veo 3**
   - The prompt is sent to Google Cloud's Veo 3 model via the Vertex AI API.
   - Veo generates an 8-second video (with optional audio) in 16:9 format.

4. **Download & Upload**
   - The resulting video is stored in a Google Cloud Storage bucket.
   - `gsutil` is used to download the video locally.
   - The video is then uploaded directly in reply to the original tweet.

5. **Automated Response**
   - The bot replies with a short message and attaches the video, tagging the original user.

---

## ⚙️ Requirements

- Python 3.8+
- Google Cloud Vertex AI access with `veo-3.0-generate-preview`
- gsutil (installed via Google Cloud SDK)
- Twitter Developer account with API access (read/write permissions)

---

## 📦 Stack

- Google Cloud (Vertex AI, Veo 3, GCS)
- Python
- Tweepy (Twitter API)
- dotenv
- gsutil (Google Cloud Storage CLI)

---

## 🚀 Example Usage

```text
@Clyp do a video of a neon-lit skatepark in space
```

⬇️ Bot replies within minutes with a generated `.mp4` clip.

---

## 💡 Use Cases

- Instant visual storytelling
- Viral social media content
- Creative prompts for digital artists
- Generative AI demos

---

## 🔒 Limitations

- Veo 3 access is currently in private preview (must be allowlisted by Google)
- Videos are limited to 8 seconds and 16:9 resolution
- gsutil must be authenticated with appropriate permissions to download videos

---

## 🧬 Project Vision

Clyp aims to redefine creative interaction on social media by enabling natural language video creation. By bridging AI video models with real-time public input (via Twitter), it opens a new dimension in generative media.

---

**This project was created to power Clyp by Gl1tch 💠**
