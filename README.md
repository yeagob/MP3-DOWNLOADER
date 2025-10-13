Free  MP3 Downloader

This is a simple web application built with Flask that allows users to download MP3 audio from YouTube videos by searching song titles or fetching tracklists from albums/artists using MusicBrainz API. It supports single songs, lists of songs, and automatic folder organization for albums or artists.
Features:

Search and download individual songs or lists.
Fetch tracklists from albums or all songs from an artist (limited to 100 unique tracks).
Dark/light mode toggle.
Progress bar for multiple downloads.
Legal notice and thanks to contributors.

Usage Instructions

Run the App:

After installation (see below), execute python app.py in your terminal.
Open a web browser and navigate to http://127.0.0.1:5000/.


Fetching Tracklists:

Enter the artist name (required for fetching all songs, optional for albums).
Enter the album name (optional; leave empty or it will fetch up to 100 songs from the artist if artist is provided).
Click "Fetch Tracklist". The textarea will populate with song titles in the format "Title - Artist".
If successful, a modal will confirm; edit the list if needed.


Downloading MP3s:

Enter song titles in the textarea (one per line) or use the fetched list.
Click "Download MP3(s)".
For multiple downloads, a progress bar shows status.
Upon completion, download links appear, and files are saved in the downloads folder (or subfolder for albums/artists).
A modal notifies when done, with file location info.


Theme Toggle:

Click the sun/moon icon in the top-right to switch between dark and light modes.



Notes:

Downloads aim for the highest quality (~320kbps equivalent, source-dependent).
Use responsibly; respect copyrights and YouTube's terms.

Installation and Execution
Windows

Install Python:

Download and install Python from python.org. Ensure you check "Add Python to PATH" during installation.


Install Dependencies:

Open Command Prompt.
Run: pip install flask yt-dlp musicbrainzngs.


Install FFmpeg:

Download from ffmpeg.org/download.html (e.g., static build for Windows).
Extract the archive and add the bin folder to your system's PATH:

Search for "Edit the system environment variables" in Start menu.
Click "Environment Variables" > Edit "Path" under System variables > Add the path to FFmpeg's bin (e.g., C:\ffmpeg\bin).


Verify: Run ffmpeg -version in Command Prompt.


Run the App:

Save the code as app.py in a folder.
In Command Prompt, navigate to the folder: cd path\to\folder.
Run: python app.py.
Access at http://127.0.0.1:5000/.



Linux

Install Python:

Most distributions have Python pre-installed. Check: python3 --version.
If not, install: sudo apt update && sudo apt install python3 python3-pip (Ubuntu/Debian) or equivalent for your distro.


Install Dependencies:

Run: pip install flask yt-dlp musicbrainzngs.


Install FFmpeg:

Run: sudo apt install ffmpeg (Ubuntu/Debian) or equivalent.
Verify: ffmpeg -version.


Run the App:

Save the code as app.py.
In terminal, navigate to the folder: cd path/to/folder.
Run: python3 app.py.
Access at http://127.0.0.1:5000/.



Mac

Install Python:

Download from python.org or use Homebrew: brew install python.


Install Dependencies:

Run: pip install flask yt-dlp musicbrainzngs.


Install FFmpeg:

Use Homebrew: brew install ffmpeg.
Verify: ffmpeg -version.


Run the App:

Save the code as app.py.
In Terminal, navigate to the folder: cd path/to/folder.
Run: python app.py.
Access at http://127.0.0.1:5000/.



Technical Explanation
This app is a Flask-based web server that integrates yt-dlp for YouTube audio extraction, MusicBrainz for tracklist fetching, and client-side JavaScript for UI interactions.
How It Works

Frontend (HTML/CSS/JS):

The UI is rendered via a Jinja-like template string in Flask.
JavaScript handles form submissions via AJAX, progress polling, theme toggling (stored in localStorage), and modal popups for feedback.
CSS provides responsive design with gradients, shadows, and mode-specific colors.


Backend (Flask Routes):

/: Handles GET for initial page and POST for downloading songs. Uses threading for background downloads to avoid blocking.
/fetch_tracklist: Fetches tracklists from MusicBrainz. If no album, fetches artist's songs (up to 100 unique). Stores in session for subfolder creation.
/status/<task_id>: Polls download progress.
/download/<path:filename>: Serves downloaded files.


Downloading Process:

yt-dlp extracts audio as MP3, aiming for best quality.
Files save to downloads or artist/album subfolder.
Progress tracked in a global dict, updated in a thread.


Dependencies:

Flask: Web framework.
yt-dlp: YouTube downloader.
musicbrainzngs: MusicBrainz API client.
FFmpeg: Required for audio conversion (installed separately).


Security/Notes:

Runs locally; no external hosting.
Sanitizes filenames to prevent issues.
Handles errors with modals.



For contributions or issues, open a pull request or issue on GitHub.

By Santiago Game Lover
