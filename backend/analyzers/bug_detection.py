import subprocess

def run_bug_detection(file_path: str) -> str:
    result = subprocess.run(["pytest", file_path], capture_output=True, text=True)
    return result.stdout
