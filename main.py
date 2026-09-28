from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_index():
    return FileResponse("index.html")

@app.get("/verify/{owner}/{repo}")
def verify_repo(owner: str, repo: str):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Repository not found")
        
    data = response.json()
    
    stars = data.get("stargazers_count", 0)
    has_description = 15 if data.get("description") else 0
    has_license = 15 if data.get("license") else 0
    language = data.get("language") or "Code"
    
    base_score = 50
    star_score = min(stars * 2, 20)
    total_score = min(base_score + star_score + has_description + has_license, 100)
    
    status = "VERIFIED CANDIDATE" if total_score >= 70 else "NEEDS IMPROVEMENT"
    
    return {
        "candidate_repo": f"{owner}/{repo}",
        "primary_language": language,
        "score": total_score,
        "status": status,
        "stars": stars
    }
