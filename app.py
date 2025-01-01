from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os

# Specify the templates folder explicitly
app = Flask(__name__, template_folder="templates")

# Define the route correctly
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        link = request.form.get("video_link")
        if link:
            try:
                yt = YouTube(link)
                stream = yt.streams.get_highest_resolution()
                download_path = stream.download(output_path="downloads")  # Specify a download folder
                return send_file(download_path, as_attachment=True)  # Offer the file for download
            except Exception as e:
                return f"An error occurred: {e}"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
