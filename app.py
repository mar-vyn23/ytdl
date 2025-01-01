from flask import Flask, render_template, request, redirect, url_for, send_file
from pytubefix import YouTube
from pytubefix.cli import on_progress
import os
import tempfile

app = Flask(__name__, template_folder="templates")

# Home route for the video link input
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        link = request.form.get("video_link")
        if link:
            try:
                # Use pytubefix to fetch video details
                yt = YouTube(link, use_oauth=True, allow_oauth_cache=True, on_progress_callback=on_progress)
                yt_title = yt.title  # Get the video title
                yt_thumbnail = yt.thumbnail_url  # Get the video thumbnail
                available_streams = yt.streams.filter(progressive=True)  # Filter for video+audio streams

                # Pass video data to the template via URL query string
                return redirect(url_for('video_details', link=link))
            except Exception as e:
                return f"An error occurred: {e}"
    return render_template("index.html")


# Video details route for displaying video info and download options
@app.route("/video_details")
def video_details():
    link = request.args.get("link")
    if link:
        try:
            yt = YouTube(link, use_oauth=True, allow_oauth_cache=True, on_progress_callback=on_progress)
            yt_title = yt.title
            yt_thumbnail = yt.thumbnail_url
            available_streams = yt.streams.filter(progressive=True)

            # Prepare video data to be passed to the template
            video_data = {
                "title": yt_title,
                "thumbnail": yt_thumbnail,
                "streams": [
                    {"itag": stream.itag, "resolution": stream.resolution, "mime_type": stream.mime_type}
                    for stream in available_streams
                ]
            }

            return render_template("video_details.html", video_data=video_data)
        except Exception as e:
            return f"An error occurred: {e}"
    return redirect(url_for('home'))


# Download route for handling the download requests
@app.route("/download/<int:stream_id>")
def download(stream_id):
    link = request.args.get("link")
    if link:
        try:
            yt = YouTube(link, use_oauth=True, allow_oauth_cache=True, on_progress_callback=on_progress)
            stream = yt.streams.get_by_itag(stream_id)

            if stream:
                # Create a temporary directory for the file
                with tempfile.TemporaryDirectory() as temp_dir:
                    # Create a temporary file path for the video/audio
                    temp_file_path = os.path.join(temp_dir, f"{yt.title}_{stream.resolution}.mp4")

                    # Download the stream to the temporary file
                    stream.download(output_path=temp_dir, filename=os.path.basename(temp_file_path))

                    # Send the file to the browser for download
                    return send_file(
                        temp_file_path,
                        as_attachment=True,
                        download_name=f"{yt.title}_{stream.resolution}.mp4", 
                        mimetype="video/mp4"
                    )
            else:
                return f"Stream not found.", 404

        except Exception as e:
            return f"An error occurred: {e}", 500
    return f"Invalid URL or stream ID.", 400


if __name__ == "__main__":
    app.run(debug=True)
