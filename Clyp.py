
# Script developed for the Clyp project by Gl1tch – empowering video generation through Veo 3 🚀


import os
import subprocess
import tweepy
from google.cloud import aiplatform_v1beta1
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set Google credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Vertex AI credentials
PROJECT_ID = os.getenv("PROJECT_ID")
REGION = os.getenv("REGION")
MODEL_NAME = os.getenv("MODEL")

# Twitter credentials
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
TWITTER_HANDLE = os.getenv("TWITTER_HANDLE")

# Authenticate Twitter
auth = tweepy.OAuth1UserHandler(
    TWITTER_API_KEY, TWITTER_API_SECRET,
    TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET
)
twitter_api = tweepy.API(auth)

def download_from_gs(gs_uri, output_filename):
    print(f"Downloading video from: {gs_uri}")
    try:
        subprocess.run(["gsutil", "cp", gs_uri, output_filename], check=True)
        print(f"✅ Video saved as: {output_filename}")
    except subprocess.CalledProcessError:
        print("❌ Failed to download video. Check gsutil setup.")

def generate_video(prompt):
    print(f"🚀 Generating video for prompt: '{prompt}'")
    client = aiplatform_v1beta1.PredictionServiceClient()
    model_path = f"projects/{PROJECT_ID}/locations/{REGION}/publishers/google/models/{MODEL_NAME}"

    instance = {
        "prompt": prompt,
        "parameters": {
            "aspectRatio": "16:9",
            "durationSeconds": 8,
            "generateAudio": True
        }
    }

    response = client.predict(
        endpoint=model_path,
        instances=[instance],
        timeout=500
    )

    print("📨 API response received.")
    try:
        video_uri = response.predictions[0]["videoUri"]
        print(f"🎥 Video URI: {video_uri}")
        download_from_gs(video_uri, "generated_video.mp4")
        return True
    except (IndexError, KeyError):
        print("❌ videoUri not found in response.")
        return False

def respond_to_mentions():
    client = tweepy.Client(bearer_token=os.getenv("TWITTER_BEARER_TOKEN"))
    print(f"🔍 Looking for recent mentions to @{TWITTER_HANDLE}")
    mentions = client.get_users_mentions(id=client.get_user(username=TWITTER_HANDLE).data.id, max_results=5)

    if mentions.data:
        for tweet in mentions.data:
            text = tweet.text
            tweet_id = tweet.id
            author = tweet.author_id

            if f"@{TWITTER_HANDLE}" in text:
                prompt = text.replace(f"@{TWITTER_HANDLE}", "").strip()
                if prompt:
                    print(f"📢 Prompt: {prompt}")
                    if generate_video(prompt):
                        try:
                            media = twitter_api.media_upload("generated_video.mp4")
                            twitter_api.update_status(
                                status=f"Here is your video 🎬",
                                in_reply_to_status_id=tweet_id,
                                media_ids=[media.media_id_string],
                                auto_populate_reply_metadata=True
                            )
                            print(f"✅ Replied with video to tweet ID {tweet_id}")
                        except Exception as e:
                            print(f"❌ Failed to reply with video: {e}")
                else:
                    print("⚠️ Mention found, but no prompt detected.")
    else:
        print("ℹ️ No mentions found.")

if __name__ == "__main__":
    respond_to_mentions()

# Script developed for the Clyp project by Gl1tch – empowering video generation through Veo 3 🚀

