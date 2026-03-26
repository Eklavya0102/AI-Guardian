from fastapi import FastAPI
from fastapi import UploadFile, File
from pydantic import BaseModel
from typing import List, Optional

from phishing_detector import analyze_email
from link_checker import analyze_link
from job_scam_detector import analyze_job_scam
from deepfake_detector import analyze_image
from logs import log_event, get_logs
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Guardian Backend")

# Basic CORS for dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class EmailRequest(BaseModel):
    text: str


class LinkRequest(BaseModel):
    url: str


class JobRequest(BaseModel):
    text: str


@app.post("/analyze-email")
async def analyze_email_endpoint(req: EmailRequest):
    result = analyze_email(req.text)
    log_event("analyze_email", {"length": len(req.text), **result})
    return result


@app.post("/scan-link/")
async def scan_link_endpoint(req: LinkRequest):
    result = analyze_link(req.url)
    log_event("scan_link", {"url": req.url, **result})
    return result


@app.post("/detect-job-scam")
async def detect_job_scam_endpoint(req: JobRequest):
    result = analyze_job_scam(req.text)
    log_event("detect_job_scam", {"length": len(req.text), **result})
    return result


@app.post("/detect-deepfake")
async def detect_deepfake_endpoint(file: UploadFile = File(...)):
    content = await file.read()
    result = analyze_image(content)
    log_event("detect_deepfake", {"content_length": len(content), **result})
    return result


@app.get("/logs")
async def get_logs_endpoint(limit: int = 50):
    logs = get_logs(limit)
    return {"logs": logs}


if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
