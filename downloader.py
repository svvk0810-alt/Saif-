import os
import yt_dlp

from config import DOWNLOADS_DIR


class VideoDownloader:

    def __init__(self):

        self.base_opts = {
            "quiet": True,
            "noplaylist": True,
            "nocheckcertificate": True,
            "ignoreerrors": False,
            "no_warnings": True,
            "restrictfilenames": False,

            # تحسين الاتصال
            "socket_timeout": 60,
            "retries": 5,
            "fragment_retries": 5,
            "file_access_retries": 3,

            # تجاوز بعض مشاكل المواقع
            "http_headers": {
                "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }
        }


    def info(self, url):

        opts = self.base_opts.copy()

        with yt_dlp.YoutubeDL(opts) as ydl:

            data = ydl.extract_info(
                url,
                download=False
            )

        return data



    def qualities(self, url):

        info = self.info(url)

        formats = []

        added = set()

        for f in info.get("formats", []):

            height = f.get("height")

            if not height:
                continue

            if height in added:
                continue

            if f.get("vcodec") == "none":
                continue

            added.add(height)

            formats.append({

                "id": f["format_id"],
                "text": f"🎥 {height}p"

            })


        formats.sort(
            key=lambda x:
            int(
                x["text"]
                .split()[1]
                .replace("p", "")
            )
        )


        return info, formats




    def download_video(
        self,
        url,
        format_id,
        progress_hook=None
    ):

        output = os.path.join(
            DOWNLOADS_DIR,
            "%(title)s.%(ext)s"
        )


        opts = self.base_opts.copy()


        opts.update({

            "format":
            f"{format_id}+bestaudio/best",

            "merge_output_format":
            "mp4",

            "outtmpl":
            output,

            "writethumbnail": True,

            "postprocessors": [
                {
                    "key": "FFmpegThumbnailsConvertor",
                    "format": "jpg"
                }
            ],

            "progress_hooks":
            [
                progress_hook
            ]
            if progress_hook
            else []

        })


        with yt_dlp.YoutubeDL(opts) as ydl:

            info = ydl.extract_info(
                url,
                download=True
            )


            filename = ydl.prepare_filename(info)

            root = os.path.splitext(filename)[0]

            mp4 = root + ".mp4"


            thumbnail = None


            for ext in [
                "jpg",
                "webp",
                "png"
            ]:

                thumb = root + "." + ext

                if os.path.exists(thumb):

                    thumbnail = thumb

                    break


            return {
                "file": mp4,
                "thumbnail": thumbnail,
                "title": info.get(
                    "title",
                    "فيديو"
                )
            }




    def download_audio(
        self,
        url,
        progress_hook=None
    ):


        output = os.path.join(
            DOWNLOADS_DIR,
            "%(title)s.%(ext)s"
        )


        opts = self.base_opts.copy()


        opts.update({

            "format":
            "bestaudio",

            "outtmpl":
            output,


            "progress_hooks":
            [
                progress_hook
            ]
            if progress_hook
            else [],


            "postprocessors":
            [

                {

                    "key":
                    "FFmpegExtractAudio",

                    "preferredcodec":
                    "mp3",

                    "preferredquality":
                    "320",

                }

            ]

        })



        with yt_dlp.YoutubeDL(opts) as ydl:

            info = ydl.extract_info(
                url,
                download=True
            )


            filename = ydl.prepare_filename(
                info
            )


            root = os.path.splitext(
                filename
            )[0]


            return {
                "file": root + ".mp3",
                "thumbnail": info.get("thumbnail"),
                "title": info.get("title")
            }




    def progress(status):

        if status["status"] == "downloading":

            downloaded = status.get(
                "downloaded_bytes",
                0
            )


            total = (
                status.get("total_bytes")
                or
                status.get(
                    "total_bytes_estimate",
                    0
                )
            )


            speed = status.get(
                "speed",
                0
            )


            eta = status.get(
                "eta",
                0
            )


            percent = 0


            if total:
                percent = (
                    downloaded /
                    total *
                    100
                )


            print(
                f"{percent:.1f}% | "
                f"{downloaded}/{total} | "
                f"{speed} B/s | "
                f"ETA {eta}s"
            )



        elif status["status"] == "finished":

            print(
                "Download Finished"
            )