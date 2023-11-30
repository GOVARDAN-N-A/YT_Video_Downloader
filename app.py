from flask import Flask, render_template, request
from pytube import YouTube
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_resolutions', methods=['POST'])
def get_resolutions():
    if request.method == 'POST':
        url = request.form.get('url', '')
        video = YouTube(url)
        
        # Filter unique resolutions
        unique_resolutions = set()
        resolutions = []
        for stream in video.streams.filter(file_extension="mp4").order_by("resolution"):
            resolution = f"{stream.resolution}: {stream.filesize / (1024 * 1024):.2f} MB"
            if resolution not in unique_resolutions:
                resolutions.append(resolution)
                unique_resolutions.add(resolution)

        title = video.title
        duration = video.length
        return render_template('index.html', resolutions=resolutions, title=title, duration=duration, url=url)

@app.route('/download', methods=['POST'])
def download():
    if request.method == 'POST':
        url = request.form.get('url', '')
        resolution = request.form.get('resolution', '')
        video = YouTube(url)
        selected_video = video.streams.filter(res=resolution, file_extension="mp4").first()
        selected_video.download()
        message = f"Finished Downloading {video.title} in {resolution}"
        return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run()
