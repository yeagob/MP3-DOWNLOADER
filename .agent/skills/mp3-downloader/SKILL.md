---
name: mp3-downloader
description: Downloader for MP3 audio files and tracklists from YouTube/MusicBrainz. Activates when the user requests downloading songs, extracting audio from YouTube videos/searches, fetching tracklists from artists or albums, or managing local music downloads. This skill MUST be used whenever the user mentions downloading music, songs, or tracklists, including Spanish requests containing keywords like 'bajar', 'descargar', 'canción', 'música', or related tracklist queries.
---

# MP3 Downloader Skill

This skill allows agents to download MP3 music tracks from YouTube and fetch metadata/tracklists from MusicBrainz using the local `MP3-DOWNLOADER` utility located at `c:\Users\santi\MP3-DOWNLOADER`.

## Capabilities

1. **Automated MP3 Extraction**: Converts YouTube video search queries directly into high-quality `320kbps` equivalent MP3 files saved locally.
2. **MusicBrainz Album/Artist Tracklist Fetching**: Automatically looks up release tracklists or artist top recordings and lists them or feeds them directly into the downloader.
3. **Smart Folder Organization**: Downloads are automatically stored in clean folders: `downloads/<Artist - Album>/` or `downloads/<Artist>/` depending on the query context.
4. **Flask Web GUI**: Local web-based control panel at `http://127.0.0.1:5000/`.

---

## Core Agent Workflows

### 1. Download Individual Tracks or Queries
To download one or multiple songs, run the CLI directly in the workspace directory `c:\Users\santi\MP3-DOWNLOADER`:
```bash
python app.py "Bohemian Rhapsody Queen" "Stairway to Heaven Led Zeppelin"
```
The utility will search YouTube, grab the best audio, extract it to MP3 using FFmpeg, and save it in the `downloads/` folder.

### 2. Fetch Album/Artist Tracklists (Without Downloading)
To look up a tracklist from MusicBrainz to show the user or inspect before downloading, use the `--list-only` option:
```bash
python app.py --artist "The Beatles" --album "Abbey Road" --list-only
```
This prints the tracks as `Title - Artist` to stdout.

### 3. Download Full Album or Artist Collection
To fetch and download an entire album or artist's recordings (up to 100 unique) into a dedicated folder:
* **For an Album**:
  ```bash
  python app.py --artist "Pink Floyd" --album "The Dark Side of the Moon"
  ```
  Saves files under `downloads/Pink Floyd - The Dark Side of the Moon/`.
* **For All of an Artist's Major Songs**:
  ```bash
  python app.py --artist "Michael Jackson" --album "all"
  ```
  Saves files under `downloads/Michael Jackson/`.

### 4. Running the Web Server
If a user wants to use the graphical web application, start the server:
```bash
python app.py --server
```
Then direct the user to access `http://127.0.0.1:5000/`.

---

## Troubleshooting & Verification

* **Error: ModuleNotFoundError**:
  If python packages are missing, run:
  ```bash
  pip install -r requirements.txt
  ```
* **Error: FFmpeg not found**:
  Ensure FFmpeg is installed and added to the PATH system environment variable. If missing, download a static build and add its `bin` folder to the system PATH.
* **Rate Limits / 403 Forbidden**:
  The CLI auto-updates `yt-dlp` at startup to bypass common botanical restrictions. If errors persist, run:
  ```bash
  pip install --upgrade yt-dlp
  ```
