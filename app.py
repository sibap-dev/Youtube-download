from flask import Flask, render_template, request, send_file
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)

# Function to download YouTube video
def download_youtube_video(url):
    try:
        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save video in the "downloads" folder
            'format': 'best',  # Download the best quality available
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return filename
    except Exception as e:
        print(f"Error: {e}")
        return None

# Route for the landing page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_url = request.form.get("video_url")
        if video_url:
            # Download the video
            file_path = download_youtube_video(video_url)
            if file_path:
                # Send the file to the user for download
                return send_file(file_path, as_attachment=True)
            else:
                return "Error: Unable to download the video. Please check the URL and try again."
        else:
            return "Please enter a valid YouTube URL."
    return render_template("index.html")

# Ensure the "downloads" folder exists
if not os.path.exists("downloads"):
    os.makedirs("downloads")

# Vercel requires the app to be assigned to a variable named `app`
if __name__ == "__main__":
    app.run(debug=True)