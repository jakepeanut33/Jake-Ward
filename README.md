# Core Boys Funny Clips — YouTube Shorts Automation

Automatically posts **3 Shorts per day** to a YouTube channel. Each post is
built from a source YouTube clip: the segment is downloaded, reformatted into a
vertical 9:16 Short (with an optional blurred background and a burned-in
caption), and uploaded via the YouTube Data API. A scheduled GitHub Actions
workflow runs the whole thing on cron — no server to keep running.

> ⚠️ **Before you use this:** re-uploading other people's videos can violate
> YouTube's Terms of Service and copyright law unless you own the footage, have
> the creator's permission, or have a clear fair-use / transformative basis.
> Channels that repost clips without rights get struck and terminated. Make sure
> you're allowed to use the source content. This tool gives you the plumbing; the
> rights are your responsibility.

---

## How it works

```
data/queue.json  ->  download segment (yt-dlp)  ->  make vertical Short (ffmpeg)  ->  upload (YouTube API)  ->  mark posted
```

- **`data/queue.json`** is the list of clips to post, newest at the bottom. Each
  run posts the first clip that hasn't been posted yet and marks it done.
- **GitHub Actions** runs `python -m src.pipeline` three times a day and commits
  the updated queue back to the repo so it remembers what's already posted.

## One-time setup

### 1. Get YouTube API credentials
1. Go to the [Google Cloud Console](https://console.cloud.google.com/), create a
   project, and enable **YouTube Data API v3**.
2. Configure the **OAuth consent screen** (User type: External; add your own
   Google account as a Test user).
3. Create an **OAuth client ID** of type **Desktop app** and download the JSON.
   Save it as `client_secret.json` in the repo root (it's git-ignored).

### 2. Mint a refresh token
On your own computer (this opens a browser to log in to the channel's account):
```bash
pip install -r requirements.txt
python scripts/authorize.py
```
It prints three values: `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN`.

### 3. Add the secrets to GitHub
In your repo: **Settings → Secrets and variables → Actions → New repository
secret**, and add all three from the previous step.

### 4. Configure the channel
Edit `config/settings.yaml` — channel name, hashtags, privacy
(`public`/`unlisted`/`private`), background style (`blur`/`crop`/`pad`), etc.
Start with `privacy_status: unlisted` while you test.

### 5. Fill the queue
Edit `data/queue.json`. Each entry needs a source URL and start/end timestamps:
```json
{
  "id": "any-unique-id",
  "source_url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "start": "00:01:05",
  "end": "00:01:52",
  "title": "Core Boys lose it at the worst time 😂",
  "caption": "wait for it...",
  "posted": false,
  "posted_at": null,
  "video_id": null
}
```
Keep `start`/`end` under ~58 seconds apart (Shorts max out at 60s).

## Test it without posting

Build a Short locally without uploading (no credentials needed, but you need
`ffmpeg` and `yt-dlp` installed):
```bash
python -m src.pipeline --dry-run
```
The finished file lands in `work/`. Watch it, tweak `config/settings.yaml`, repeat.

## Go live
Once secrets are set and the queue has clips, the workflow runs on its own. You
can also trigger a post immediately from the repo's **Actions** tab →
**Post Core Boys Short** → **Run workflow**.

### Changing the schedule
Edit the three `cron:` lines in `.github/workflows/post-shorts.yml`. Cron is in
**UTC**. The defaults are roughly 9am / 3pm / 8pm US Central.

## Auto-discovery: clip the top-performing videos automatically
Instead of hand-feeding URLs, the pipeline can find top videos itself and queue
clips of them. When the queue runs empty, it refills from whatever sources you
enable in `config/settings.yaml`:

**`discovery`** — finds the most-viewed videos and clips them:
- `mode: search` — most-viewed videos for your `keywords` (best for a niche like
  "core boys funny").
- `mode: trending` — the regional "most popular" chart.
- Filters by `min_views`, `max_source_duration_seconds`, and (search mode)
  `published_within_days`, then auto-clips a `clip_length_seconds` window
  starting `clip_offset_seconds` in (to skip intros).

Discovery needs a **YouTube Data API key** (public-data read; separate from the
upload OAuth token). Create one in the same Google Cloud project under
**APIs & Services → Credentials → API key**, and add it as the `YT_API_KEY`
GitHub secret.

**`auto_source`** — instead/also pulls the latest uploads from specific channels
you list.

> ⚠️ **Auto-clipping the current top videos is the riskiest mode.** Those are
> exactly the videos most likely to be Content-ID matched and claimed, and a
> channel that only reposts other people's hits is the classic strike-and-ban
> pattern. Use it with creators who allow reuse, or add genuine transformation.
>
> Also note: the tool can find *which* video is popular, but not *which 50
> seconds* are the good part — it takes a fixed window. Hand-picked timestamps
> in `data/queue.json` still make much better Shorts.

## Project layout
```
config/settings.yaml                 channel + formatting config (non-secret)
data/queue.json                      the clips to post + posted state
src/pipeline.py                      orchestrates one post (entrypoint)
src/downloader.py                    yt-dlp wrapper (segment download + listing)
src/clipper.py                       ffmpeg vertical-Short formatting
src/uploader.py                      YouTube Data API upload
src/queue_manager.py                 read/write/advance the queue
src/auto_source.py                   optional channel auto-sourcing
scripts/authorize.py                 one-time OAuth helper
.github/workflows/post-shorts.yml    the 3x/day scheduler
```

## Limits & notes
- The YouTube API gives ~6 uploads/day of headroom on the default quota
  (each upload costs ~1600 of 10,000 daily units), so 3/day is comfortable.
- If uploads land as `private`, your OAuth app is probably still in "Testing"
  mode — that's a Google account setting, not a bug here.
- ffmpeg and yt-dlp are installed automatically in the GitHub Actions run.
