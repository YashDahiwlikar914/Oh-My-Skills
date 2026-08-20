# Social Media Archiving

Patterns for public YouTube, TikTok, and Instagram material. Platforms change
their access controls frequently, so expect these tools to break and check for
updates before debugging anything else.

Doctrine that applies to all three:

- Public, non-credentialed access only, unless the user supplies documented
  authorization.
- Never use credentialed sessions by default. Logged-in scraping changes the
  legal posture under CFAA and the platforms' terms.
- For research or journalism at scale, prefer the official programs when
  eligible: Meta Content Library for Instagram, TikTok Research API for TikTok.
- Metadata-first. Extract titles, descriptions, timestamps, and counts before
  downloading any media. Often the metadata is all the task needs.

## YouTube With yt-dlp

```python
import yt_dlp
from pathlib import Path

def download_video_metadata(url: str) -> dict:
    """Extract metadata without downloading video."""
    ydl_opts = {
        'skip_download': True,
        'quiet': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            'title': info.get('title'),
            'description': info.get('description'),
            'duration': info.get('duration'),
            'upload_date': info.get('upload_date'),
            'view_count': info.get('view_count'),
            'channel': info.get('channel'),
            'thumbnail': info.get('thumbnail'),
        }

def download_video(url: str, output_dir: Path, audio_only: bool = False) -> Path:
    """Download video or audio."""
    output_template = str(output_dir / '%(title)s.%(ext)s')

    ydl_opts = {
        'outtmpl': output_template,
        'quiet': True,
    }

    if audio_only:
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        if audio_only:
            filename = filename.rsplit('.', 1)[0] + '.mp3'
        return Path(filename)

def get_transcript(url: str) -> list[dict]:
    """Extract auto-generated or manual subtitles."""
    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        subtitles = info.get('subtitles', {})
        auto_captions = info.get('automatic_captions', {})

        # Prefer manual subtitles over auto-generated
        subs = subtitles.get('en') or auto_captions.get('en')
        if not subs:
            return []

        for sub in subs:
            if sub['ext'] in ['vtt', 'json3']:
                # Download and parse subtitle file
                # Implementation depends on format
                pass

        return []
```

## Instagram With instaloader

The class below refuses credentialed sessions unless the caller passes
`allow_authenticated_session=True`, which is the code-level enforcement of the
doctrine above.

```python
import instaloader
from pathlib import Path

class InstagramScraper:
    def __init__(self, username: str = None, session_file: str = None,
                 allow_authenticated_session: bool = False):
        self.loader = instaloader.Instaloader(
            download_videos=True,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=True,
            compress_json=False,
        )

        if session_file and not allow_authenticated_session:
            raise ValueError(
                'Authenticated sessions require explicit user approval and '
                'documented authorization'
            )
        if allow_authenticated_session and session_file and Path(session_file).exists():
            if not username:
                raise ValueError('A username is required for a session file')
            self.loader.load_session_from_file(username, session_file)

    def get_profile_posts(self, username: str, limit: int = 50) -> list[dict]:
        """Get recent posts from a profile."""
        profile = instaloader.Profile.from_username(self.loader.context, username)
        posts = []

        for i, post in enumerate(profile.get_posts()):
            if i >= limit:
                break

            posts.append({
                'shortcode': post.shortcode,
                'url': f'https://instagram.com/p/{post.shortcode}/',
                'caption': post.caption,
                'timestamp': post.date_utc.isoformat(),
                'likes': post.likes,
                'comments': post.comments,
                'is_video': post.is_video,
                'video_url': post.video_url if post.is_video else None,
            })

        return posts

    def download_post(self, shortcode: str, output_dir: Path):
        """Download a single post's media."""
        post = instaloader.Post.from_shortcode(self.loader.context, shortcode)
        self.loader.download_post(post, target=str(output_dir))
```

## TikTok With yt-dlp

```python
def scrape_tiktok_profile(username: str, output_dir: Path, limit: int = 50) -> list[dict]:
    """Scrape TikTok profile videos."""
    profile_url = f'https://tiktok.com/@{username}'

    ydl_opts = {
        'quiet': True,
        'extract_flat': True,  # Don't download, just get info
        'playlistend': limit,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(profile_url, download=False)
        videos = []

        for entry in info.get('entries', []):
            videos.append({
                'id': entry.get('id'),
                'title': entry.get('title'),
                'url': entry.get('url'),
                'timestamp': entry.get('timestamp'),
                'view_count': entry.get('view_count'),
            })

        return videos

def download_tiktok_video(url: str, output_dir: Path) -> Path:
    """Download a single TikTok video."""
    ydl_opts = {
        'outtmpl': str(output_dir / '%(id)s.%(ext)s'),
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return Path(ydl.prepare_filename(info))
```
