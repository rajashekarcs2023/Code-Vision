import subprocess

def run_quality_analysis(file_path: str) -> str:
    result = subprocess.run(["pylint", file_path], capture_output=True, text=True)
    return result.stdout
