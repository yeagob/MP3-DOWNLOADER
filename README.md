# Free MP3 Downloader

This is a simple web application built with Flask that allows users to download MP3 audio by searching song titles or fetching tracklists from albums/artists using MusicBrainz API. It supports single songs, lists of songs, and automatic folder organization for albums or artists.

**Features:**
- Search and download individual songs or lists.
- Fetch tracklists from albums or all songs from an artist (limited to 100 unique tracks).
- Dark/light mode toggle.
- Progress bar for multiple downloads.
- Legal notice and thanks to contributors.

## Installation and Execution

### Windows

1. **Install Python**:
   - Download and install Python from [python.org](https://www.python.org/downloads/). Ensure you check "Add Python to PATH" during installation. Python 3.8 or higher is recommended.

2. **Install FFmpeg** (Required for audio extraction):
   - Download a static build from [ffmpeg.org/download.html](https://ffmpeg.org/download.html) (e.g., from git.ffmpeg.org or a trusted source like gyan.dev).
   - Extract the archive to a folder (e.g., `C:\ffmpeg`).
   - Add the `bin` folder to your system's PATH:
     - Search for "Edit the system environment variables" in the Start menu.
     - Click "Environment Variables" > Under "System variables", edit "Path" > Add the path to FFmpeg's `bin` (e.g., `C:\ffmpeg\bin`).
   - Restart Command Prompt to apply changes.
   - Verify: Run `ffmpeg -version` in Command Prompt. If it fails, double-check the PATH.

3. **Install Python Dependencies**:
   - Navigate to the project folder in Command Prompt: `cd path\to\MP3-DOWNLOADER`
   - Run: `pip install -r requirements.txt`
   - This will install Flask, yt-dlp, and musicbrainzngs automatically.
   - If errors occur (e.g., pip not found), ensure Python is in PATH and run `python -m ensurepip` if needed.

4. **Run the App**:
   - In the project folder, run: `python app.py`
   - Access at `http://127.0.0.1:5000/`
   - If errors persist (e.g., FFmpeg not found), verify FFmpeg installation and PATH. For yt-dlp issues, ensure no antivirus blocks it.

**Optional - Create batch files for convenience**:
   - Create `install.bat`:
     ```
     @echo off
     echo Installing dependencies...
     pip install -r requirements.txt
     if %errorlevel% neq 0 (
         echo Error installing packages. Ensure pip is installed and try again.
         pause
     ) else (
         echo Installation complete!
         pause
     )
     ```

   - Create `run.bat`:
     ```
     @echo off
     echo Running the app...
     python app.py
     pause
     ```

### Linux

1. **Install Python**:
   - Most distributions have Python pre-installed. Check: `python3 --version`.
   - If not, install: `sudo apt update && sudo apt install python3 python3-pip` (Ubuntu/Debian) or equivalent for your distro (e.g., `sudo dnf install python3 python3-pip` for Fedora). Use Python 3.8 or higher.

2. **Install FFmpeg** (Required for audio extraction):
   - Run: `sudo apt install ffmpeg` (Ubuntu/Debian) or equivalent (e.g., `sudo dnf install ffmpeg` for Fedora).
   - Verify: `ffmpeg -version`.

3. **Install Python Dependencies**:
   - Navigate to the project folder: `cd path/to/MP3-DOWNLOADER`
   - Run: `pip install -r requirements.txt` (or `pip3 install -r requirements.txt`)
   - This will install Flask, yt-dlp, and musicbrainzngs automatically.

4. **Run the App**:
   - In the project folder, run: `python3 app.py`
   - Access at `http://127.0.0.1:5000/`
   - If errors occur, ensure all packages installed successfully and FFmpeg is in PATH.

### Mac

1. **Install Python**:
   - Download from [python.org](https://www.python.org/downloads/) or use Homebrew: `brew install python`. Use Python 3.8 or higher.

2. **Install FFmpeg** (Required for audio extraction):
   - Install Homebrew if not present: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`.
   - Run: `brew install ffmpeg`.
   - Verify: `ffmpeg -version`.

3. **Install Python Dependencies**:
   - Navigate to the project folder: `cd path/to/MP3-DOWNLOADER`
   - Run: `pip install -r requirements.txt`
   - This will install Flask, yt-dlp, and musicbrainzngs automatically.

4. **Run the App**:
   - In the project folder, run: `python app.py`
   - Access at `http://127.0.0.1:5000/`
   - If errors occur, ensure Homebrew is updated (`brew update`) and all packages installed.

**General Troubleshooting**:
- If pip fails, upgrade it: `python -m pip install --upgrade pip`.
- For "ModuleNotFoundError", rerun: `pip install -r requirements.txt`.
- Ensure no firewalls/antivirus block yt-dlp or FFmpeg.
- The app requires internet for YouTube/MusicBrainz access.

## Usage Instructions

### Run the App
- After installation (see below), execute `python app.py` in your terminal.
- Open a web browser and navigate to `http://127.0.0.1:5000/`.

### Fetching Tracklists
- Enter the artist name (required for fetching all songs, optional for albums).
- Enter the album name (optional; leave empty or it will fetch up to 100 songs from the artist if artist is provided).
- Click "Fetch Tracklist". The textarea will populate with song titles in the format "Title - Artist".
- If successful, a modal will confirm; edit the list if needed.

### Downloading MP3s
- Enter song titles in the textarea (one per line) or use the fetched list.
- Click "Download MP3(s)".
- For multiple downloads, a progress bar shows status.
- Upon completion, download links appear, and files are saved in the `downloads` folder (or subfolder for albums/artists).
- A modal notifies when done, with file location info.

### Theme Toggle
- Click the sun/moon icon in the top-right to switch between dark and light modes.

**Notes:**
- Downloads aim for the highest quality (~320kbps equivalent, source-dependent).
- Use responsibly; respect copyrights and YouTube's terms.


## Technical Explanation

This app is a Flask-based web server that integrates yt-dlp for YouTube audio extraction, MusicBrainz for tracklist fetching, and client-side JavaScript for UI interactions.

### How It Works

#### Frontend (HTML/CSS/JS)
- The UI is rendered via a Jinja-like template string in Flask.
- JavaScript handles form submissions via AJAX, progress polling, theme toggling (stored in localStorage), and modal popups for feedback.
- CSS provides responsive design with gradients, shadows, and mode-specific colors.

#### Backend (Flask Routes)
- `/`: Handles GET for initial page and POST for downloading songs. Uses threading for background downloads to avoid blocking.
- `/fetch_tracklist`: Fetches tracklists from MusicBrainz. If no album, fetches artist's songs (up to 100 unique). Stores in session for subfolder creation.
- `/status/<task_id>`: Polls download progress.
- `/download/<path:filename>`: Serves downloaded files.

#### Downloading Process
- yt-dlp extracts audio as MP3, aiming for best quality.
- Files save to `downloads` or artist/album subfolder.
- Progress tracked in a global dict, updated in a thread.

#### Dependencies
- **Flask**: Web framework.
- **yt-dlp**: YouTube downloader.
- **musicbrainzngs**: MusicBrainz API client.
- **FFmpeg**: Required for audio conversion (installed separately).

#### Security/Notes
- Runs locally; no external hosting.
- Sanitizes filenames to prevent issues.
- Handles errors with modals.

For contributions or issues, open a pull request or issue on GitHub.

By Santiago Game Lover
