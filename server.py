import tempfile
from pathlib import Path
from urllib.parse import urlparse
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from yt_dlp import YoutubeDL

app=FastAPI()
BASE=Path(__file__).parent

def valid_url(url):
    try:
        p=urlparse(url)
        return p.scheme in ('http','https') and p.netloc.lower() in {'x.com','www.x.com','twitter.com','www.twitter.com'}
    except: return False

@app.get('/',response_class=HTMLResponse)
async def home(): return (BASE/'index.html').read_text(encoding='utf-8')

@app.post('/download')
async def download(request:Request):
    data=await request.json(); url=str(data.get('url','')).strip()
    if not valid_url(url): raise HTTPException(400,'Geçerli bir X URLsi gerekli.')
    folder=Path(tempfile.mkdtemp(prefix='xvid_'))
    try:
        opts={'outtmpl':str(folder/'%(id)s.%(ext)s'),'format':'bv*+ba/b','merge_output_format':'mp4','noplaylist':True,'quiet':True,'no_warnings':True,'restrictfilenames':True}
        with YoutubeDL(opts) as ydl:
            info=ydl.extract_info(url,download=True)
            expected=Path(ydl.prepare_filename(info))
            candidates=list(folder.glob(expected.stem+'.*'))
        if not candidates: raise RuntimeError('Video dosyası oluşturulamadı.')
        return FileResponse(candidates[0],filename='x-video.mp4',media_type='video/mp4')
    except Exception as e: raise HTTPException(400,str(e))
