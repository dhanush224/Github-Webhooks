from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "ReviewFlow backend running"}

@app.post("/webhooks/github")
async def github_webhook(request: Request):
    payload = await request.json()

    action = payload.get("action")
    repo = payload.get("repository", {}).get("full_name")
    pr_number = payload.get("pull_request", {}).get("number")

    print("Action:", action)
    print("Repo:", repo)
    print("PR Number:", pr_number)

    return {
        "action": action,
        "repo": repo,
        "pr_number": pr_number
    }