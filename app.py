from flask import Flask, render_template, request, send_file
from pytubefix import YouTube
from pytubefix.cli import on_progress
import io

# Specify the templates folder explicitly
app = Flask(__name__, template_folder="templates")

# Define the route correctly
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        link = request.form.get("video_link")
        if link:
            try:
                # Using OAuth with PoToken enabled
                yt = YouTube(link, use_oauth=True, allow_oauth_cache=True, on_progress_callback=on_progress)
                yt_title = yt.title  # Get the video title for feedback
                stream = yt.streams.get_highest_resolution()

                # Create a bytes buffer to stream the file without saving it to the server
                video_buffer = io.BytesIO()
                stream.stream_to_buffer(video_buffer)
                video_buffer.seek(0)

                # Send the file directly to the browser for download
                return send_file(
                    video_buffer,
                    as_attachment=True,
                    download_name=f"{yt_title}.mp4",
                    mimetype="video/mp4"
                )
            except Exception as e:
                return f"An error occurred: {e}"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
