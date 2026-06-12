from fastapi import FastAPI, HTTPException
import yt_dlp

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Link Extractor API is running. Use /extract?url=YOUR_LINK"}

@app.get("/extract")
def extract_link(url: str):
    # yt-dlp ke options. Brutal focus on just getting the direct URL.
    ydl_opts = {
        'format': 'best', # Single file format jisme audio aur video dono ho
        'quiet': True,
        'skip_download': True, # Video download nahi karni hai, bas link chahiye
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Webpage ko analyze kar
            info_dict = ydl.extract_info(url, download=False)
            
            # Direct raw link nikalo
            direct_url = info_dict.get("url", None)
            title = info_dict.get("title", "Unknown Title")
            
            if not direct_url:
                raise HTTPException(status_code=400, detail="Could not extract direct streamable link.")
                
            return {
                "status": "success",
                "title": title,
                "original_url": url,
                "direct_url": direct_url
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))