from flask import Flask, render_template, request, redirect, url_for, send_file
from pytubefix import YouTube
from pytubefix.cli import on_progress
import os
import tempfile

app = Flask(__name__, template_folder="templates")

# Define the common resolutions in the desired order
common_resolutions = ["360p", "480p", "720p", "1080p", "1440p", "2160p", "4320p"]

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
                available_streams = yt.streams.filter(progressive=False, file_extension="mp4")  # Filter for mp4 streams

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
            available_streams = yt.streams.filter(file_extension="mp4")  # Get all mp4 streams

            # Filter streams based on resolution and order them accordingly
            filtered_video_streams = sorted(
                [
                    {"itag": stream.itag, "resolution": stream.resolution, "mime_type": stream.mime_type}
                    for stream in available_streams
                    if stream.resolution in common_resolutions and stream.type == "video"
                ],
                key=lambda stream: common_resolutions.index(stream["resolution"])  # Sorting by resolution order
            )

            filtered_audio_streams = [
                {"itag": stream.itag, "mime_type": stream.mime_type, "abr": stream.abr}
                for stream in available_streams
                if stream.type == "audio"
            ]

            # Prepare video and audio data to be passed to the template
            video_data = {
                "title": yt_title,
                "thumbnail": yt_thumbnail,
                "video_streams": filtered_video_streams,
                "audio_streams": filtered_audio_streams,
            }

            return render_template("video_details.html", video_data=video_data)
        except Exception as e:
            return f"An error occurred: {e}"
    return redirect(url_for('home'))


# Download route for handling the download requests
@app.route("/download/<int:stream_id>")
def download(stream_id):
    link = request.args.get("link")  # Get the link from query string
    if link:
        try:
            yt = YouTube(link, use_oauth=True, allow_oauth_cache=True, on_progress_callback=on_progress)
            stream = yt.streams.get_by_itag(stream_id)

            if stream:
                # Create a temporary directory for the file
                temp_dir = tempfile.mkdtemp()  # Persist the temp directory until manual cleanup
                temp_file_path = os.path.join(temp_dir, f"{yt.title}_{stream.resolution if stream.resolution else 'audio'}.mp4")

                # Download the stream to the temporary file
                stream.download(output_path=temp_dir, filename=os.path.basename(temp_file_path))

                # Use a generator to serve the file
                def generate():
                    with open(temp_file_path, "rb") as file:
                        while chunk := file.read(4096):
                            yield chunk

                response = app.response_class(
                    generate(),
                    mimetype="video/mp4",
                    headers={
                        "Content-Disposition": f"attachment; filename={yt.title}_{stream.resolution if stream.resolution else 'audio'}.mp4"
                    },
                )

                # Cleanup after the response is sent
                @response.call_on_close
                def cleanup():
                    try:
                        if os.path.exists(temp_file_path):
                            os.remove(temp_file_path)  # Remove the temporary file
                        if os.path.exists(temp_dir):
                            os.rmdir(temp_dir)  # Remove the temporary directory
                    except Exception as cleanup_error:
                        print(f"Cleanup error: {cleanup_error}")

                return response
            else:
                return "Stream not found.", 404

        except Exception as e:
            return f"An error occurred: {e}", 500
    return "Invalid URL or stream ID.", 400




if __name__ == "__main__":
    app.run(debug=True)
