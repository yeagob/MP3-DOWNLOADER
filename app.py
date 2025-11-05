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
            release = musicbrainzngs.get_release_by_id(release_id, includes=['recordings', 'artist-credits'])
            
            tracks = release['release']['medium-list'][0]['track-list']
            track_lines = []
            for track in tracks:
                title = track['recording']['title']
                track_artist = track['recording'].get('artist-credit-phrase', artist or release['release'].get('artist-credit-phrase', 'Unknown'))
                track_lines.append(f"{title} - {track_artist}")
            
            prefill_text = '\n'.join(track_lines)
            
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
            # CORREGIDO: 'artists' → 'artist-credits'
            recordings = musicbrainzngs.browse_recordings(artist=artist_id, limit=100, includes=['artist-credits'])
            
            track_set = set()
            for rec in recordings['recording-list']:
                title = rec['title']
                # CORREGIDO: .get() con fallback
                track_artist = rec.get('artist-credit-phrase') or artist
                track_set.add(f"{title} - {track_artist}")
            
            prefill_text = '\n'.join(sorted(track_set))
            
            album_folder = sanitize_filename(artist)

        session['album_folder'] = album_folder
        session['prefill_text'] = prefill_text
        session['artist'] = artist
        session['album'] = album
    
    except Exception as e:
        errors.append(f"Failed to fetch tracklist: {str(e)}")
    
    return jsonify({'prefill_text': prefill_text, 'errors': errors})
