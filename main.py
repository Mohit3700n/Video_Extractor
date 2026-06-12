from fastapi import FastAPI, HTTPException
import yt_dlp

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Extractor is running!"}

@app.get("/extract")
def extract_link(url: str):
    # Yahan se 'format' line hata di hai taaki yt-dlp crash na ho
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'no_warnings': True,
        'cookiefile': 'cookies.txt', # Cookies abhi bhi zaroori hain bot bypass ke liye
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Ye ab saare formats extract karega bina crash hue
            info_dict = ydl.extract_info(url, download=False)
            
            direct_url = None
            
            # Smart Filtering: Wo link dhoondho jisme Audio (acodec) aur Video (vcodec) dono hon
            if 'formats' in info_dict:
                combined_formats = [
                    f for f in info_dict['formats'] 
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none'
                ]
                if combined_formats:
                    # List ke end me normally best quality (720p/360p) hoti hai
                    direct_url = combined_formats[-1].get('url')
            
            # Fallback (Agar Facebook/Instagram ho jahan formats array alag hota hai)
            if not direct_url:
                direct_url = info_dict.get('url', None)
                
            if not direct_url:
                raise HTTPException(status_code=400, detail="Could not extract direct streamable link.")
                
            return {
                "status": "success",
                "direct_url": direct_url
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))