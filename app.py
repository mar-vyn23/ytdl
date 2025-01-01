from flask import Flask, render_template, request, send_file
from pytubefix import YouTube
from pytubefix.cli import on_progress
import os
import tempfile

# Specify the templates folder explicitly
app = Flask(__name__, template_folder="templates")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        link = request.form.get("video_link")
        if link:
            try:
                # Using OAuth with PoToken enabled
                yt = YouTube(link, use_oauth=True, allow_oauth_cache=True, on_progress_callback=on_progress)
                yt_title = yt.title  # Get the video title for feedback
                stream = yt.streams.get_highest_resolution()  # Get the highest resolution stream

                # Create a temporary file to store the video/audio
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
                    temp_file_path = temp_file.name
                    
                    # Download the audio stream to the temporary file
                    stream.download(output_path=os.path.dirname(temp_file_path), filename=os.path.basename(temp_file_path))

                    # Send the file to the browser for download
                    response = send_file(
                        temp_file_path,
                        as_attachment=True,
                        download_name=f"{yt_title}.mp4", 
                        mimetype="video/mp4"
                    )

                    # Cleanup the temporary file after sending it
                    @response.call_on_close
                    def remove_file():
                        try:
                            os.remove(temp_file_path)
                        except Exception as e:
                            print(f"Error deleting file: {e}")
                    
                    return response

            except Exception as e:
                return f"An error occurred: {e}"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
