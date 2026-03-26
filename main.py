from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import yt_dlp
import os

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Video Downloader</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial; text-align: center; padding: 20px; background: #f5f5f5; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
            input, button { padding: 12px; margin: 10px; font-size: 16px; }
            input { width: 70%; border: 2px solid #ddd; border-radius: 5px; }
            button { background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #0056b3; }
            #result { margin-top: 20px; }
            .hidden { display: none; }
            .spinner { border: 4px solid #f3f3f3; border-top: 4px solid #007bff; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 20px auto; }
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            img { max-width: 100%; border-radius: 5px; }
            .download-btn { background: #28a745; margin: 5px; display: inline-block; padding: 10px 20px; text-decoration: none; color: white; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📹 Social Media Video Downloader</h1>
            <p>Paste any video link from TikTok, Instagram, X, or Facebook</p>
            <input type="text" id="url" placeholder="Paste URL here...">
            <button onclick="download()">Download Video</button>
            <div id="loading" class="hidden">
                <div class="spinner"></div>
                <p>Processing... Please wait 5-10 seconds</p>
            </div>
            <div id="result"></div>
        </div>

        <script>
            async function download() {
                const url = document.getElementById('url').value;
                if (!url) {
                    alert('Please paste a URL');
                    return;
                }
                
                document.getElementById('loading').classList.remove('hidden');
                document.getElementById('result').innerHTML = '';
                
                try {
                    const res = await fetch(`/api/download?url=${encodeURIComponent(url)}`);
                    const data = await res.json();
                    
                    document.getElementById('loading').classList.add('hidden');
                    
                    if (data.success) {
                        let html = `<img src="${data.thumbnail}" alt="thumbnail"><br>`;
                        html += `<h3>${data.title}</h3>`;
                        html += `<div>`;
                        data.formats.forEach(f => {
                            html += `<a href="${f.url}" class="download-btn" target="_blank">Download ${f.quality}</a> `;
                        });
                        html += `</div>`;
                        document.getElementById('result').innerHTML = html;
                    } else {
                        document.getElementById('result').innerHTML = `<p style="color:red">❌ Error: ${data.error}</p>`;
                    }
                } catch(e) {
                    document.getElementById('loading').classList.add('hidden');
                    document.getElementById('result').innerHTML = `<p style="color:red">❌ Failed to process. Check URL and try again.</p>`;
                }
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

@app.get("/api/download")
async def download_video(url: str):
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            formats = []
            for f in info.get('formats', []):
                if f.get('height'):
                    formats.append({
                        'quality': f'{f["height"]}p',
                        'format': f.get('ext', 'mp4'),
                        'url': f['url']
                    })
            
            # Remove duplicates (keep highest quality for each resolution)
            seen = set()
            unique_formats = []
            for f in formats:
                if f['quality'] not in seen:
                    seen.add(f['quality'])
                    unique_formats.append(f)
            
            return {
                'success': True,
                'title': info.get('title', 'Video'),
                'thumbnail': info.get('thumbnail', ''),
                'formats': unique_formats[:5]
            }
    except Exception as e:
        return {'success': False, 'error': str(e)}

@app.get("/health")
def health():
    return {"status": "ok"}

# THIS PART IS IMPORTANT - Makes Railway run the app
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
@app.get("/api/download")
async def download_video(url: str):
    try:
        # TikTok-specific headers
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            formats = []
            for f in info.get('formats', []):
                if f.get('height'):
                    formats.append({
                        'quality': f'{f["height"]}p',
                        'format': f.get('ext', 'mp4'),
                        'url': f['url']
                    })
            
            return {
                'success': True,
                'title': info.get('title', 'Video'),
                'thumbnail': info.get('thumbnail', ''),
                'formats': formats[:5]
            }
    except Exception as e:
        return {'success': False, 'error': str(e)}
