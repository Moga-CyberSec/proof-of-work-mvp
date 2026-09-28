from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests

app = FastAPI(title="Proof-of-Work Code Analyzer")

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r") as f:
        return f.read()

@app.get("/analyze/{owner}/{repo}")
def analyze_repo(owner: str, repo: str):
    repo_url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(repo_url)
    
    if response.status_code != 200:
        return {"error": "Repository not found or is private."}
    
    data = response.json()
    
    readme_check = requests.get(f"https://raw.githubusercontent.com/{owner}/{repo}/main/README.md")
    has_readme = readme_check.status_code == 200
    
    score = 40
    if has_readme:
        score += 30
    if data.get("language") == "Python":
        score += 15
    if data.get("stargazers_count", 0) > 0:
        score += 15

    return {
        "candidate_repo": f"{owner}/{repo}",
        "primary_language": data.get("language", "Not specified"),
        "has_documentation": has_readme,
        "proof_of_work_score": f"{score}/100",
        "badge_status": "VERIFIED CANDIDATE" if score >= 70 else "NEEDS IMPROVEMENT"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)