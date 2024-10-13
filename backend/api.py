import os
import subprocess
from fastapi import FastAPI, HTTPException
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import ast
import re

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

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
def home():
    return {"message": "Welcome to Code Analysis Tool"}

@app.get("/files/")
def list_files():
    files = os.listdir(UPLOAD_DIR)
    if not files:
        return {"message": "No files to process"}
    return {"files": files}

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
    """Run basic bug detection on the file."""
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        
        tree = ast.parse(content)
        issues = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Try) and not node.handlers:
                issues.append("Empty except block found")
            elif isinstance(node, ast.Except) and isinstance(node.type, ast.Name) and node.type.id == 'Exception':
                issues.append("Bare except clause found")

        if issues:
            return f"Potential bugs found in {file_path}:\n" + "\n".join(issues)
        else:
            return f"No obvious bugs detected in {file_path}."
    except Exception as e:
        return f"Failed to detect bugs in {file_path}. Error: {str(e)}"

def optimize_performance(file_path):
    """Basic performance optimization suggestions."""
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        
        tree = ast.parse(content)
        suggestions = []

        for node in ast.walk(tree):
            if isinstance(node, ast.For):
                suggestions.append("Consider using list comprehension instead of for loop where applicable")
            elif isinstance(node, ast.If) and isinstance(node.test, ast.Compare) and len(node.test.ops) > 1:
                suggestions.append("Multiple comparisons in if statement. Consider simplifying")

        if suggestions:
            return f"Performance optimization suggestions for {file_path}:\n" + "\n".join(suggestions)
        else:
            return f"No obvious performance optimizations found for {file_path}."
    except Exception as e:
        return f"Failed to analyze performance for {file_path}. Error: {str(e)}"



def audit_security(file_path):
    """
    Perform a comprehensive security audit on the file, checking for compliance
    with HIPAA, SOC 2, PCI DSS, and GDPR.
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        
        tree = ast.parse(content)
        vulnerabilities = []

        # General security checks
        vulnerabilities.extend(check_general_security(tree))

        # HIPAA compliance checks
        vulnerabilities.extend(check_hipaa_compliance(tree, content))

        # SOC 2 and PCI DSS compliance checks
        vulnerabilities.extend(check_soc2_pci_compliance(tree, content))

        # GDPR compliance checks
        vulnerabilities.extend(check_gdpr_compliance(tree, content))

        if vulnerabilities:
            return f"Security vulnerabilities found in {file_path}:\n" + "\n".join(vulnerabilities)
        else:
            return f"No obvious security vulnerabilities detected in {file_path}."
    except Exception as e:
        return f"Failed to perform security audit on {file_path}. Error: {str(e)}"

def check_general_security(tree):
    vulnerabilities = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in ['eval', 'exec']:
                    vulnerabilities.append(f"Potentially unsafe use of {node.func.id}() detected")
            elif isinstance(node.func, ast.Attribute):
                if node.func.attr == 'subprocess':
                    vulnerabilities.append("Use of subprocess detected. Ensure proper input sanitization")
    return vulnerabilities

def check_hipaa_compliance(tree, content):
    vulnerabilities = []
    
    # Check for unencrypted data transmission
    if 'http://' in content and 'https://' not in content:
        vulnerabilities.append("HIPAA: Unencrypted data transmission detected. Use HTTPS instead of HTTP")

    # Check for hardcoded patient information
    patient_info_pattern = r'\b(patient|medical|health)\s*=\s*[\'"][^\'"]+[\'"]\s*'
    if re.search(patient_info_pattern, content, re.IGNORECASE):
        vulnerabilities.append("HIPAA: Potential hardcoded patient information detected")

    # Check for logging of sensitive information
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr in ['debug', 'info', 'warning', 'error', 'critical']:
                vulnerabilities.append("HIPAA: Logging detected. Ensure no sensitive patient data is being logged")

    return vulnerabilities

def check_soc2_pci_compliance(tree, content):
    vulnerabilities = []
    
    # Check for hardcoded credentials
    credential_pattern = r'\b(password|api_key|secret)\s*=\s*[\'"][^\'"]+[\'"]\s*'
    if re.search(credential_pattern, content, re.IGNORECASE):
        vulnerabilities.append("SOC 2/PCI DSS: Hardcoded credentials detected")

    # Check for insecure cryptographic algorithms
    weak_crypto = ['md5', 'sha1']
    for algo in weak_crypto:
        if algo in content.lower():
            vulnerabilities.append(f"SOC 2/PCI DSS: Weak cryptographic algorithm ({algo}) detected")

    # Check for proper error handling
    try_count = sum(1 for node in ast.walk(tree) if isinstance(node, ast.Try))
    except_count = sum(1 for node in ast.walk(tree) if isinstance(node, ast.ExceptHandler))
    if try_count > except_count:
        vulnerabilities.append("SOC 2/PCI DSS: Potential improper error handling detected")

    return vulnerabilities

def check_gdpr_compliance(tree, content):
    vulnerabilities = []
    
    # Check for personal data processing without consent
    personal_data_pattern = r'\b(name|email|address|phone|birthdate)\s*=\s*'
    if re.search(personal_data_pattern, content, re.IGNORECASE):
        vulnerabilities.append("GDPR: Personal data processing detected. Ensure user consent is obtained")

    # Check for data retention policies
    if 'delete' not in content.lower() and 'remove' not in content.lower():
        vulnerabilities.append("GDPR: No apparent data deletion mechanism. Implement data retention policies")

    # Check for cross-border data transfers
    transfer_keywords = ['transfer', 'send', 'transmit']
    for keyword in transfer_keywords:
        if keyword in content.lower():
            vulnerabilities.append("GDPR: Potential cross-border data transfer detected. Ensure compliance with GDPR transfer rules")

    return vulnerabilities

def refactor_code(file_path):
    """Basic code refactoring suggestions."""
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        
        tree = ast.parse(content)
        suggestions = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and len(node.body) > 20:
                suggestions.append(f"Function '{node.name}' is long. Consider breaking it into smaller functions")
            elif isinstance(node, ast.ClassDef) and len(node.body) > 30:
                suggestions.append(f"Class '{node.name}' is large. Consider splitting it into multiple classes")

        if suggestions:
            return f"Refactoring suggestions for {file_path}:\n" + "\n".join(suggestions)
        else:
            return f"No obvious refactoring suggestions for {file_path}."
    except Exception as e:
        return f"Failed to analyze for refactoring in {file_path}. Error: {str(e)}"



def generate_openai_queries(analysis_result: str, analysis_type: str):
    """Generate relevant queries based on analysis result using OpenAI's Chat API."""
    
    # Define improved prompts based on analysis type
    if analysis_type == "code_quality":
        prompt = f"""Based on this code quality analysis result: '{analysis_result}', suggest 3 critical and actionable questions for developers. Each question should:
        1. Address a specific issue mentioned in the analysis.
        2. Propose a concrete improvement or solution.
        3. Consider long-term maintainability and best practices.
        Focus on areas such as code structure, naming conventions, documentation, and adherence to PEP 8 guidelines."""

    elif analysis_type == "bug_detection":
        prompt = f"""Analyzing this bug detection result: '{analysis_result}', formulate 3 targeted questions for developers. Each question should:
        1. Pinpoint a specific bug or potential issue mentioned.
        2. Inquire about the root cause and potential impact.
        3. Suggest a debugging approach or possible fix.
        Consider various bug types such as logic errors, runtime exceptions, and edge cases."""

    elif analysis_type == "performance":
        prompt = f"""Examining this performance optimization result: '{analysis_result}', create 3 in-depth questions to improve code efficiency. Each question should:
        1. Target a specific performance bottleneck identified in the analysis.
        2. Explore algorithmic improvements or optimizations.
        3. Consider trade-offs between performance, readability, and maintainability.
        Address areas like time complexity, memory usage, and resource management."""

    elif analysis_type == "security":
        prompt = f"""Given this security audit result: '{analysis_result}', formulate 3 crucial questions for the security team. Each question should:
        1. Address a specific vulnerability or security risk mentioned.
        2. Inquire about potential exploit scenarios and their severity.
        3. Explore both immediate fixes and long-term security enhancements.
        Consider aspects such as input validation, authentication, data encryption, and secure coding practices."""

    elif analysis_type == "security":
        prompt = f"""Given the following security audit result: '{analysis_result}', generate a comprehensive security analysis report. The report should include:

            1. Executive Summary:
            - Provide a high-level overview of the security audit findings.
            - Highlight the most critical vulnerabilities or compliance issues.

            2. Detailed Analysis (address each of the following):
            a. HIPAA Compliance:
                - Identify any potential violations of patient data privacy.
                - Assess the security of health information transmission and storage.
            b. SOC 2 and PCI DSS Compliance:
                - Evaluate the handling of sensitive financial data and credentials.
                - Analyze the robustness of cryptographic implementations.
            c. GDPR Compliance:
                - Examine personal data processing practices and consent mechanisms.
                - Assess data retention policies and cross-border transfer compliance.
            d. General Security Best Practices:
                - Review input validation, authentication methods, and access controls.
                - Analyze the use of potentially unsafe functions or libraries.

            3. Risk Assessment:
            - For each identified vulnerability:
                * Describe potential exploit scenarios.
                * Assess the severity and potential impact on the organization.
                * Estimate the likelihood of exploitation.

            4. Remediation Plan:
            - Propose immediate fixes for critical vulnerabilities.
            - Suggest long-term security enhancements and best practices.
            - Recommend tools or processes for ongoing security monitoring.

            5. Compliance Roadmap:
            - Outline steps to achieve full compliance with relevant standards (HIPAA, SOC 2, PCI DSS, GDPR).
            - Suggest employee training programs to improve security awareness.

            6. Future Considerations:
            - Discuss emerging security threats relevant to the industry.
            - Recommend proactive measures to stay ahead of evolving security challenges.

            Ensure the report is detailed, actionable, and prioritizes issues based on their criticality. Use clear, concise language suitable for both technical and non-technical stakeholders.
            """

    elif analysis_type == "refactoring":
        prompt = f"""Based on this code refactoring analysis: '{analysis_result}', devise 3 strategic questions for the development team. Each question should:
        1. Target a specific area of the code that needs restructuring.
        2. Explore how the proposed refactoring will improve code quality or maintainability.
        3. Consider the impact on existing functionality and potential risks.
        Address topics such as design patterns, modularity, code reuse, and adherence to SOLID principles."""

    try:
        # Call OpenAI's ChatCompletion endpoint
        response = client.chat.completions.create(
            model="gpt-4o",  # Use "gpt-4" for best results
            messages=[
                {"role": "system", "content": "You are an expert software engineer specializing in code analysis and best practices. Provide insightful and actionable advice."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=2000,
            temperature=0.7,  # Adjust for creativity vs consistency
        )

        # Extract and return the OpenAI response
        query_response = response.choices[0].message.content.strip()
        print(f"OpenAI response: {query_response}")
        
        return query_response

    except Exception as e:
        error_message = f"Failed to get response from OpenAI. Error: {str(e)}"
        print(error_message)
        return error_message
