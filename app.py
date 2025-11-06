from flask import Flask, request, send_from_directory, render_template_string, jsonify, session
import yt_dlp
from yt_dlp.utils import sanitize_filename
import os
import musicbrainzngs
import threading
import uuid
import time
import sys
import subprocess

# Auto-update yt-dlp and clear cache at startup
subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'yt-dlp'], capture_output=True)
subprocess.run([sys.executable, '-m', 'yt_dlp', '--rm-cache-dir'], capture_output=True)

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Needed for session

# Set user agent for MusicBrainz
musicbrainzngs.set_useragent("youtube-mp3-downloader", "1.0", "https://example.com")

# Base directory to save downloaded MP3 files
BASE_DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(BASE_DOWNLOAD_FOLDER):
    os.makedirs(BASE_DOWNLOAD_FOLDER)

# Global tasks dictionary for progress (task_id: {'done': 0, 'total': 0, 'status': '', 'links': [], 'errors': []}})
tasks = {}

# HTML template with dark mode by default, theme switch, legal notice at bottom, and modal for messages
FORM_TEMPLATE = '''
<!doctype html>
<html>
<head>
    <title>YouTube to MP3 Downloader</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            margin: 20px;
            padding: 20px;
            max-width: 700px;
            margin: auto;
            border: 1px solid;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            transition: background 0.3s, color 0.3s;
        }
        body.dark {
            background: linear-gradient(135deg, #1e293b, #0f172a);
            color: #e2e8f0;
            border-color: #475569;
        }
        body.light {
            background: linear-gradient(135deg, #f4f7f9, #e0e7ff);
            color: #2c3e50;
            border-color: #cbd5e1;
        }
        h1 {
            text-align: center;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }
        body.dark h1 { color: #60a5fa; }
        body.light h1 { color: #1e40af; }
        h2 {
            color: #3b82f6;
        }
        body.dark h2 { color: #93c5fd; }
        body.light h2 { color: #3b82f6; }
        form {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        input[type="text"], textarea {
            width: 100%;
            padding: 12px;
            border: 1px solid;
            border-radius: 6px;
            margin-bottom: 12px;
            font-size: 16px;
            transition: background 0.3s, color 0.3s, border-color 0.3s;
        }
        body.dark input[type="text"], body.dark textarea {
            background-color: #334155;
            color: #e2e8f0;
            border-color: #475569;
        }
        body.light input[type="text"], body.light textarea {
            background-color: #f8fafc;
            color: #2c3e50;
            border-color: #94a3b8;
        }
        button {
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 16px;
            margin-bottom: 12px;
            transition: transform 0.2s, background 0.3s;
        }
        body.dark button {
            background: linear-gradient(135deg, #60a5fa, #3b82f6);
        }
        body.light button {
            background: linear-gradient(135deg, #3b82f6, #2563eb);
        }
        button:hover {
            transform: scale(1.05);
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            margin: 12px 0;
            padding: 12px;
            border-radius: 6px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        body.dark li { background-color: #475569; }
        body.light li { background-color: #eff6ff; }
        a {
            text-decoration: none;
        }
        body.dark a { color: #f87171; }
        body.light a { color: #ef4444; }
        a:hover {
            text-decoration: underline;
        }
        .error {
            font-weight: bold;
        }
        body.dark .error { color: #f87171; }
        body.light .error { color: #ef4444; }
        #progress-container {
            display: none;
            width: 100%;
            border-radius: 6px;
            padding: 12px;
            margin-bottom: 20px;
        }
        body.dark #progress-container { background-color: #334155; }
        body.light #progress-container { background-color: #e0e7ff; }
        #progress-bar {
            width: 0%;
            height: 20px;
            border-radius: 6px;
            transition: width 0.3s;
        }
        body.dark #progress-bar { background: linear-gradient(135deg, #60a5fa, #3b82f6); }
        body.light #progress-bar { background: linear-gradient(135deg, #3b82f6, #2563eb); }
        #progress-text {
            text-align: center;
            margin-top: 8px;
            font-weight: bold;
        }
        #theme-switch {
            position: absolute;
            top: 20px;
            right: 20px;
            cursor: pointer;
            font-size: 24px;
        }
        .thanks-section, .legal-notice {
            margin-top: 20px;
            padding: 12px;
            border-radius: 6px;
            border: 1px solid;
        }
        body.dark .thanks-section, body.dark .legal-notice {
            background-color: #334155;
            border-color: #475569;
        }
        body.light .thanks-section, body.light .legal-notice {
            background-color: #dbeafe;
            border-color: #bfdbfe;
        }
        /* Modal styles */
        .modal {
            display: none;
            position: fixed;
            z-index: 1;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.4);
            padding-top: 60px;
        }
        .modal-content {
            margin: auto;
            padding: 20px;
            border: 1px solid #888;
            width: 80%;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        body.dark .modal-content {
            background-color: #334155;
            color: #e2e8f0;
        }
        body.light .modal-content {
            background-color: #fefefe;
            color: #2c3e50;
        }
        .close {
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
        }
        .close:hover,
        .close:focus {
            color: black;
            text-decoration: none;
            cursor: pointer;
        }
        body.dark .close { color: #e2e8f0; }
        body.dark .close:hover { color: #fff; }
    </style>
    <script>
        function toggleTheme() {
            const body = document.body;
            if (body.classList.contains('dark')) {
                body.classList.remove('dark');
                body.classList.add('light');
                localStorage.setItem('theme', 'light');
                document.getElementById('theme-switch').innerHTML = '🌙';
            } else {
                body.classList.remove('light');
                body.classList.add('dark');
                localStorage.setItem('theme', 'dark');
                document.getElementById('theme-switch').innerHTML = '☀️';
            }
        }

        window.onload = function() {
            const theme = localStorage.getItem('theme') || 'dark';
            document.body.classList.add(theme);
            document.getElementById('theme-switch').innerHTML = theme === 'dark' ? '☀️' : '🌙';

            // Modal close handlers
            var modal = document.getElementById('myModal');
            var span = document.getElementsByClassName("close")[0];
            span.onclick = function() {
                modal.style.display = "none";
            }
            window.onclick = function(event) {
                if (event.target == modal) {
                    modal.style.display = "none";
                }
            }
        };

        function showModal(message) {
            document.getElementById('modal-message').innerHTML = message.replace(/\\n/g, '<br>');
            document.getElementById('myModal').style.display = "block";
        }

        function startDownload(formId) {
            const form = document.getElementById(formId);
            if (formId === 'fetch-form' && form.artist.value.trim() === '' && form.album.value.trim() === '') {
                showModal('Please provide at least an artist or album name.');
                return false;
            }
            if (formId === 'fetch-form' && form.album.value.trim() === '' && form.artist.value.trim() !== '') {
                form.album.value = 'all';
            }
            const formData = new FormData(form);
            const xhr = new XMLHttpRequest();
            xhr.open('POST', form.action);
            xhr.onload = function() {
                if (xhr.status === 200) {
                    const response = JSON.parse(xhr.responseText);
                    if (response.task_id) {
                        document.getElementById('progress-container').style.display = 'block';
                        pollProgress(response.task_id);
                    } else if (response.prefill_text) {
                        document.getElementById('title-textarea').value = response.prefill_text;
                        if (response.errors && response.errors.length > 0) {
                            showModal(response.errors.join('\\n'));
                        } else {
                            showModal('Tracklist fetched successfully!');
                        }
                    }
                }
            };
            xhr.send(formData);
            return false;
        }

        function pollProgress(taskId) {
            const xhr = new XMLHttpRequest();
            xhr.open('GET', '/status/' + taskId);
            xhr.onload = function() {
                if (xhr.status === 200) {
                    const progress = JSON.parse(xhr.responseText);
                    const bar = document.getElementById('progress-bar');
                    const text = document.getElementById('progress-text');
                    const percent = (progress.done / progress.total) * 100;
                    bar.style.width = percent + '%';
                    text.innerHTML = progress.status + ' (' + progress.done + '/' + progress.total + ')';

                    if (progress.done < progress.total) {
                        setTimeout(() => pollProgress(taskId), 1000);
                    } else {
                        const downloadsDiv = document.getElementById('downloads');
                        downloadsDiv.innerHTML = '';
                        if (progress.links.length > 0) {
                            let ul = '<h2>Downloads Ready:</h2><ul>';
                            progress.links.forEach(link => {
                                ul += '<li><a href="' + link.link + '" download>' + link.name + '</a></li>';
                            });
                            ul += '</ul>';
                            downloadsDiv.innerHTML += ul;
                        }
                        if (progress.errors.length > 0) {
                            let ul = '<h2 class="error">Errors:</h2><ul class="error">';
                            progress.errors.forEach(err => {
                                ul += '<li>' + err + '</li>';
                            });
                            ul += '</ul>';
                            downloadsDiv.innerHTML += ul;
                        }
                        showModal('Downloads completed! Files are saved in the \\'downloads\\' folder in the app\\'s directory. For albums or artists, check the subfolder named after the artist/album if applicable.');
                    }
                }
            };
            xhr.send();
        }
    </script>
</head>
<body class="dark">
    <div id="theme-switch" onclick="toggleTheme()">☀️</div>
    <h1>Enter Song Title(s) or Fetch Album/Artist Tracklist</h1>
    <p>Enter one song title or multiple separated by new lines, or fetch an album's or artist's tracklist.</p>
    
    <!-- Form for fetching album tracklist -->
    <form id="fetch-form" method="post" action="/fetch_tracklist" onsubmit="return startDownload('fetch-form');">
        <input type="text" name="artist" placeholder="Artist (optional for album, required for all songs)" value="{{ artist or '' }}">
        <input type="text" name="album" placeholder="Album name (optional, leave empty for all artist's songs)">
        <button type="submit">Fetch Tracklist</button>
    </form>
    
    <!-- Main form for downloading -->
    <form id="download-form" method="post" action="/" onsubmit="return startDownload('download-form');">
        <textarea id="title-textarea" name="title" placeholder="Song title or list..." style="height: 750px;">{{ prefill_text }}</textarea>
        <button type="submit">Download MP3(s)</button>
    </form>
    
    <div id="progress-container">
        <div id="progress-bar"></div>
        <div id="progress-text">Starting...</div>
    </div>
    
    <div id="downloads">
        {% if download_links %}
            <h2>Downloads Ready:</h2>
            <ul>
                {% for dl in download_links %}
                    <li><a href="{{ dl.link }}" download>{{ dl.name }}</a></li>
                {% endfor %}
            </ul>
        {% endif %}
        {% if errors %}
            <h2 class="error">Errors:</h2>
            <ul class="error">
                {% for err in errors %}
                    <li>{{ err }}</li>
                {% endfor %}
            </ul>
        {% endif %}
    </div>

    <div class="thanks-section">
        <h2>Thanks to the Creators</h2>
        <ul>
            <li><a href="https://y2meta.tube/youtube-to-mp3/" target="_blank">Y2meta</a> - Inspiration for YouTube to MP3 conversion.</li>
            <li><a href="https://github.com/yt-dlp/yt-dlp" target="_blank">yt-dlp</a> - Powerful YouTube downloader library.</li>
            <li><a href="https://musicbrainz.org/" target="_blank">MusicBrainz</a> - Open music encyclopedia for tracklists.</li>
            <li><a href="https://flask.palletsprojects.com/" target="_blank">Flask</a> - Lightweight web framework.</li>
            <li><a href="https://ffmpeg.org/" target="_blank">FFmpeg</a> - Multimedia framework for audio extraction.</li>
        </ul>
    </div>

    <div class="legal-notice">
        <h2>Legal Notice</h2>
        <p>We are using the services of Y2meta. Is it legal to use our YouTube to MP3 Downloader? Our Y2meta tool is completely legal to use on your device. We respect all YouTube channel owners; it depends on your needs.</p>
        <p>This process is legal because we handle everything locally on your device through open-source tools, accessing YouTube via public means.</p>
    </div>

    <!-- The Modal -->
    <div id="myModal" class="modal">
        <div class="modal-content">
            <span class="close">&times;</span>
            <p id="modal-message"></p>
        </div>
    </div>
</body>
</html>
'''

def download_task(queries, task_id, album_folder=None):
    tasks[task_id]['links'] = []
    tasks[task_id]['errors'] = []
    tasks[task_id]['total'] = len(queries)
    tasks[task_id]['done'] = 0
    tasks[task_id]['status'] = 'Downloading...'

    download_folder = BASE_DOWNLOAD_FOLDER
    if album_folder:
        download_folder = os.path.join(BASE_DOWNLOAD_FOLDER, album_folder)
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

    for query in queries:
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }],
                'quiet': True,
                'no_warnings': True,
                # Anti-bot configuration to avoid 403 Forbidden errors
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-us,en;q=0.5',
                    'Sec-Fetch-Mode': 'navigate',
                },
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'web'],
                        'skip': ['hls', 'dash']
                    }
                },
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch1:{query}", download=False)['entries'][0]
                video_title = info['title']

            sanitized_title = sanitize_filename(video_title)
            expected_filename = f"{sanitized_title}.mp3"

            ydl_opts['outtmpl'] = os.path.join(download_folder, '%(title)s.%(ext)s')

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([f"ytsearch1:{query}"])

            # Adjust link to include subfolder if present
            link_filename = expected_filename if not album_folder else os.path.join(album_folder, expected_filename)
            download_link = f"/download/{link_filename.replace(os.sep, '/')}"
            tasks[task_id]['links'].append({'name': video_title + '.mp3', 'link': download_link})

        except Exception as e:
            tasks[task_id]['errors'].append(f"Failed to download '{query}': {str(e)}")

        tasks[task_id]['done'] += 1
        tasks[task_id]['status'] = f"Downloaded {tasks[task_id]['done']}/{tasks[task_id]['total']}"
        time.sleep(0.5)  # Simulate some delay for progress visibility

    tasks[task_id]['status'] = 'Completed'

@app.route('/', methods=['GET', 'POST'])
def index():
    download_links = []
    errors = []
    prefill_text = session.get('prefill_text', '')
    artist = session.get('artist', '')
    album = session.get('album', '')
    
    if request.method == 'POST':
        input_text = request.form['title']
        if input_text:
            queries = [q.strip() for q in input_text.split('\n') if q.strip()]
            task_id = str(uuid.uuid4())
            tasks[task_id] = {}
            album_folder = session.get('album_folder', None)
            threading.Thread(target=download_task, args=(queries, task_id), kwargs={'album_folder': album_folder}).start()
            return jsonify({'task_id': task_id})

    session.pop('prefill_text', None)
    session.pop('album_folder', None)
    return render_template_string(FORM_TEMPLATE, download_links=download_links, errors=errors, prefill_text=prefill_text, artist=artist, album=album)

@app.route('/fetch_tracklist', methods=['POST'])
def fetch_tracklist():
    artist = request.form.get('artist', '').strip()
    album = request.form.get('album', '').strip()
    prefill_text = ''
    errors = []
    album_folder = None
    
    try:
        if not artist and not album:
            raise ValueError("Provide at least an artist or album name.")

        if album and album.lower() != 'all':
            # Search for album
            search_params = {'release': album}
            if artist:
                search_params['artist'] = artist
            
            result = musicbrainzngs.search_releases(**search_params, limit=1)
            if not result['release-list']:
                raise ValueError("No album found.")
            
            release_id = result['release-list'][0]['id']
            release = musicbrainzngs.get_release_by_id(release_id, includes=['recordings', 'artists'])
            
            tracks = release['release']['medium-list'][0]['track-list']
            track_lines = []
            for track in tracks:
                title = track['recording']['title']
                track_artist = track['recording'].get('artist-credit-phrase', artist or release['release']['artist-credit-phrase'])
                track_lines.append(f"{title} - {track_artist}")
            
            prefill_text = '\n'.join(track_lines)
            
            # Set album folder name
            folder_name = f"{artist} - {album}" if artist else album
            album_folder = sanitize_filename(folder_name)

        else:
            # Fetch all songs by artist (limit to 100 unique)
            if not artist:
                raise ValueError("Artist is required when fetching all songs.")
            
            result = musicbrainzngs.search_artists(artist=artist, limit=1)
            if not result['artist-list']:
                raise ValueError("No artist found.")
            
            artist_id = result['artist-list'][0]['id']
            recordings = musicbrainzngs.browse_recordings(artist=artist_id, limit=100, includes=['artists'])
            
            track_set = set()
            for rec in recordings['recording-list']:
                title = rec['title']
                track_artist = rec.get('artist-credit-phrase', artist)
                track_set.add(f"{title} - {track_artist}")
            
            prefill_text = '\n'.join(sorted(track_set))
            
            # Set folder name to artist
            album_folder = sanitize_filename(artist)

        session['album_folder'] = album_folder
        session['prefill_text'] = prefill_text
        session['artist'] = artist
        session['album'] = album
    
    except Exception as e:
        errors.append(f"Failed to fetch tracklist: {str(e)}")
    
    # Return JSON for JS to update textarea and show modal
    return jsonify({'prefill_text': prefill_text, 'errors': errors})

@app.route('/status/<task_id>')
def get_status(task_id):
    if task_id in tasks:
        return jsonify(tasks[task_id])
    return jsonify({'error': 'Task not found'}), 404

@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory(BASE_DOWNLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
