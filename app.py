from flask import Flask, render_template, request, send_file
from downloader import VideoDownloader
import os

app = Flask(__name__)

downloader = VideoDownloader()

VIDEOS = {}


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        url = request.form.get("url")

        if not url:
            return render_template(
                "index.html",
                error="❌ ضع رابط الفيديو"
            )

        try:
            info, formats = downloader.qualities(url)

            video_id = str(len(VIDEOS))

            VIDEOS[video_id] = {
                "url": url,
                "formats": formats
            }

            return render_template(
                "index.html",
                info=info,
                formats=formats,
                video_id=video_id
            )

        except Exception as e:

            return render_template(
                "index.html",
                error=f"❌ {e}"
            )


    return render_template("index.html")


@app.route("/download/<video_id>/<format_id>")
def download(video_id, format_id):

    try:

        data = VIDEOS[video_id]

        result = downloader.download_video(
            data["url"],
            format_id
        )

        return send_file(
            result["file"],
            as_attachment=True
        )

    except Exception as e:

        return f"❌ خطأ: {e}"


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080
    )