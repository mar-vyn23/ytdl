# YouTube Video Downloader

This project is a simple web application built with Flask that allows users to input a YouTube video link and download the video in various resolutions. It uses the `pytubefix` library to interact with YouTube videos and retrieve video data. Users can download video and audio streams in MP4 format based on their resolution and preferences.

## Features

- **Video Link Input**: Users can input a YouTube video link to fetch video details.
- **Resolution Selection**: The application filters available streams and displays download options for various video resolutions, including audio options.
- **Video Download**: Users can download videos in MP4 format in different resolutions.
- **Thumbnail Display**: Displays the video thumbnail alongside the available stream options.

## Prerequisites

Before running the project, ensure that you have the following installed:

- Python 3.x
- Flask
- pytubefix
- Other dependencies in `requirements.txt`

### Installation

1. Clone this repository:

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:

    ```bash
    python app.py
    ```

4. Visit `http://127.0.0.1:5000/` in your browser to start using the application.

## Application Structure

The project has the following structure:


### Routes

1. **`/`** (Home Route):
    - Method: `GET`, `POST`
    - Description: Displays a form for users to input a YouTube video link. Upon submission, the link is processed, and the user is redirected to the video details page.

    ![Alt text](flaskr/static/1.PNG)

    A screenshot of the home page (index.html), showing the input field where users can paste the YouTube video URL.

2. **`/video_details`**:
    - Method: `GET`
    - Description: Displays the video title, thumbnail, and available video streams based on the provided YouTube link. Users can choose a stream to download.

    **Insert Image 2 Here:**  
    A screenshot of the video details page (video_details.html), showing the video title, thumbnail, and list of available video resolutions for download.

3. **`/download/<int:stream_id>`**:
    - Method: `GET`
    - Description: Handles the download request for the selected video stream (either audio or video) in MP4 format.

    **Insert Image 3 Here:**  
    A screenshot of the page with a progress bar or a download button that indicates the process of downloading the video/audio.

### Templates

1. **index.html**: The main page of the app, where users input the YouTube video URL.
2. **video_details.html**: Displays video title, thumbnail, and download options for video streams.

## Example Flow

1. The user inputs a YouTube video link on the home page.
2. The app fetches the video data, including title, thumbnail, and available video streams.
3. The user is redirected to the video details page to view and choose the desired resolution.
4. The user clicks the download button, and the video or audio is downloaded in the selected resolution.

**Insert Image 4 Here:**  
A visual flow diagram or a mockup showing the user flow, from entering the video link to downloading the video.

## Error Handling

- If an invalid link is provided, the application will display an error message.
- If an error occurs during the download process, an error message will be shown.

**Insert Image 5 Here:**  
A screenshot showing how the error message will appear when something goes wrong (e.g., invalid link, no stream available, etc.).

## Dependencies

- **Flask**: A micro web framework for Python.
- **pytubefix**: A library for interacting with YouTube videos and fetching streams.
- **tempfile**: Used to create temporary files for video download.

You can install the necessary dependencies by running:

```bash
pip install -r requirements.txt
