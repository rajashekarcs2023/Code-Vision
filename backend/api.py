from fastapi import FastAPI, UploadFile, File
import os

app = FastAPI()

UPLOAD_DIR = "./uploaded_files/"

# Create the upload directory if it doesn't exist
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    
    # Save the uploaded file
    with open(file_location, "wb") as f:
        content = await file.read()
        f.write(content)

    return {"filename": file.filename, "file_location": file_location}

@app.get("/github/login")
def github_login():
    # GitHub login functionality
    github_authorize_url = (
        f"https://github.com/login/oauth/authorize?client_id=your_client_id"
    )
    return {"url": github_authorize_url}

@app.get("/github/callback")
def github_callback(code: str):
    # Handle GitHub OAuth callback
    # exchange the code for an access token
    return {"message": "Callback received", "code": code}
