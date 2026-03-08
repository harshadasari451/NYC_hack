import os
import shutil
from fastapi import APIRouter, UploadFile, File, Form
from app.config import settings

router = APIRouter()


@router.post("/whatsapp")
async def upload_whatsapp(file: UploadFile = File(...)):
    """Upload a WhatsApp .txt export file."""
    if not file.filename.endswith('.txt'):
        return {"error": "Please upload a .txt file exported from WhatsApp"}
    
    save_path = settings.UPLOAD_DIR / "whatsapp" / file.filename
    with open(save_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    return {
        "status": "success",
        "filename": file.filename,
        "size": len(content),
        "path": str(save_path),
    }


@router.post("/photos")
async def upload_photos(files: list[UploadFile] = File(...)):
    """Upload photo files for avatar generation."""
    saved = []
    for file in files:
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in ['.jpg', '.jpeg', '.png', '.webp']:
            continue
        
        save_path = settings.UPLOAD_DIR / "photos" / file.filename
        with open(save_path, "wb") as f:
            content = await file.read()
            f.write(content)
        saved.append(file.filename)
    
    return {
        "status": "success",
        "files_saved": len(saved),
        "filenames": saved,
    }


@router.post("/audio-video")
async def upload_audio_video(file: UploadFile = File(...)):
    """Upload audio or video file for voice cloning."""
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ['.mp4', '.wav', '.mp3', '.m4a', '.ogg', '.webm', '.mov']:
        return {"error": f"Unsupported format: {ext}. Use mp4, wav, mp3, m4a, ogg, webm, or mov."}
    
    save_path = settings.UPLOAD_DIR / "audio_video" / file.filename
    with open(save_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    return {
        "status": "success",
        "filename": file.filename,
        "size": len(content),
        "path": str(save_path),
    }
