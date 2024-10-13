import cProfile
import pstats
from io import StringIO

def run_performance_optimization(file_path: str) -> str:
    pr = cProfile.Profile()
    pr.enable()

    # Execute the Python code in the file
    exec(open(file_path).read())

    pr.disable()
    s = StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats()
    
    return s.getvalue()
