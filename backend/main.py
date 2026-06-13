from fastapi import FastAPI, Request
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = FastAPI()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

@app.get("/")
def health_check():
    return {"status": "ReviewFlow backend running"}

@app.post("/webhooks/github")
async def github_webhook(request: Request):
    payload = await request.json()

    action = payload.get("action")
    repo = payload.get("repository", {}).get("full_name")
    pr_number = payload.get("pull_request", {}).get("number")

    repo = payload["repository"]["full_name"]
    pr_number = payload["pull_request"]["number"]
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(url, headers=headers)

    files = response.json()

    for file in files:
        print(file["filename"])
    

    print("Action:", action)
    print("Repo:", repo)
    print("PR Number:", pr_number)

    return {
        "action": action,
        "repo": repo,
        "pr_number": pr_number
    }