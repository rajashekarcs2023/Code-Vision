import os
import subprocess
import openai
from fastapi import FastAPI, HTTPException
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  # Reflex frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory where files are stored
UPLOAD_DIR = "uploaded_files"
openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure your OpenAI API key is set

@app.get("/")
def home():
    return {"message": "Welcome to Code Analysis Tool"}

# Endpoint for listing all files
@app.get("/files/")
def list_files():
    files = os.listdir(UPLOAD_DIR)
    if not files:
        return {"message": "No files to process"}
    return {"files": files}

# Code Quality Analysis
@app.get("/analyze/quality/")
def code_quality_analysis():
    files = os.listdir(UPLOAD_DIR)
    if not files:
        raise HTTPException(status_code=400, detail="No files found.")
    
    results = []
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file)
        result = analyze_code_quality(file_path)
        openai_query = generate_openai_queries(result, "code_quality")
        results.append({"file": file, "code_quality": result, "openai_query": openai_query})
    
    return {"code_quality_analysis": results}

# Bug Detection
@app.get("/analyze/bugs/")
def bug_detection():
    files = os.listdir(UPLOAD_DIR)
    if not files:
        raise HTTPException(status_code=400, detail="No files found.")
    
    results = []
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file)
        result = detect_bugs(file_path)
        openai_query = generate_openai_queries(result, "bug_detection")
        results.append({"file": file, "bug_detection": result, "openai_query": openai_query})
    
    return {"bug_detection": results}

# Performance Optimization
@app.get("/analyze/performance/")
def performance_optimization():
    files = os.listdir(UPLOAD_DIR)
    if not files:
        raise HTTPException(status_code=400, detail="No files found.")
    
    results = []
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file)
        result = optimize_performance(file_path)
        openai_query = generate_openai_queries(result, "performance")
        results.append({"file": file, "performance_optimization": result, "openai_query": openai_query})
    
    return {"performance_optimization": results}

# Security Audit
@app.get("/analyze/security/")
def security_audit():
    files = os.listdir(UPLOAD_DIR)
    if not files:
        raise HTTPException(status_code=400, detail="No files found.")
    
    results = []
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file)
        result = audit_security(file_path)
        openai_query = generate_openai_queries(result, "security")
        results.append({"file": file, "security_audit": result, "openai_query": openai_query})
    
    return {"security_audit": results}

# Code Refactoring
@app.get("/analyze/refactor/")
def code_refactoring():
    files = os.listdir(UPLOAD_DIR)
    if not files:
        raise HTTPException(status_code=400, detail="No files found.")
    
    results = []
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file)
        result = refactor_code(file_path)
        openai_query = generate_openai_queries(result, "refactoring")
        results.append({"file": file, "code_refactoring": result, "openai_query": openai_query})
    
    return {"code_refactoring": results}

### Analysis Function Stubs ###

def analyze_code_quality(file_path):
    """Run code quality analysis on the file using pylint."""
    try:
        result = subprocess.run(
            ['pylint', file_path], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
        )
        output = result.stdout

        if result.returncode != 0:
            return f"Code quality issues found in {file_path}:\n\n{output}"
        else:
            return f"No major code quality issues found in {file_path}.\n\n{output}"

    except Exception as e:
        return f"Failed to analyze code quality for {file_path}. Error: {str(e)}"

def detect_bugs(file_path):
    """Run bug detection on the file."""
    return f"Bug detection for {file_path} completed."

def optimize_performance(file_path):
    """Optimize the performance of the code."""
    return f"Performance optimization for {file_path} completed."

def audit_security(file_path):
    """Run a security audit on the file."""
    return f"Security audit for {file_path} completed."

def refactor_code(file_path):
    """Refactor the code for better structure."""
    return f"Code refactoring for {file_path} completed."

### OpenAI Integration ###
def generate_openai_queries(analysis_result, analysis_type):
    """Generate relevant queries based on analysis result using OpenAI's Chat API."""
    
    # Define system and user messages based on analysis type
    if analysis_type == "code_quality":
        prompt = f"Based on this code quality analysis result: '{analysis_result}', generate 3 critical questions to ask developers."
    elif analysis_type == "bug_detection":
        prompt = f"Based on this bug detection result: '{analysis_result}', generate 3 key queries for developers to investigate."
    elif analysis_type == "performance":
        prompt = f"Analyze this performance optimization result: '{analysis_result}' and suggest 3 questions to ask the team."
    elif analysis_type == "security":
        prompt = f"Based on this security audit result: '{analysis_result}', suggest 3 important questions to discuss with the security team."
    elif analysis_type == "refactoring":
        prompt = f"Based on this code refactoring result: '{analysis_result}', suggest 3 questions to ask the refactoring team."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or "gpt-3.5-turbo", depending on your model
            messages=[
                {"role": "system", "content": "You are an AI assistant specialized in code analysis."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=200,
        )
        return response['choices'][0]['message']['content'].strip()
    
    except Exception as e:
        return f"Failed to get response from OpenAI. Error: {str(e)}"
