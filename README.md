# X Video Downloader
Python 3.11+ ve FFmpeg ile:
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 8000
Sonra http://127.0.0.1:8000 adresini aç.
Üretimde HTTPS, rate limiting, boyut/süre sınırı ve geçici dosya temizliği eklenmelidir.
