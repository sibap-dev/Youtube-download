from flask import Flask, render_template, request, send_file
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)


def download_youtube_video(url):
    try:
        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',  
            'format': 'best',  
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return filename
    except Exception as e:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_url = request.form.get("video_url")
        if video_url:

            file_path = download_youtube_video(video_url)
            if file_path:

                return send_file(file_path, as_attachment=True)
            else:
                return "Error: Unable to download the video."
    return render_template("index.html")

if __name__ == "__main__":

    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    app.run(debug=True)