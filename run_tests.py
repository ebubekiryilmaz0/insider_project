import argparse
import sys
import subprocess
import os

def run_tests():
    parser = argparse.ArgumentParser(description="Insider QA Automation Terminal Runner")
    parser.add_argument("--browser", default="chrome", choices=["chrome", "firefox"], help="Browser to use")
    parser.add_argument("--headless", action="store_true", default=False, help="Run in headless mode")
    parser.add_argument("--smoke", action="store_true", help="Run only smoke tests")
    parser.add_argument("--parallel", action="store_true", help="Run tests in parallel")
    parser.add_argument("--reruns", type=int, default=1, help="Number of times to rerun failed tests")
    parser.add_argument("--report", action="store_true", default=True, help="Generate HTML report")

    args = parser.parse_args()
    
    # Ensure we are running from the project root directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    # Auto-detect and use the project's virtual environment if available
    python_exe = sys.executable
    venv_exe = os.path.join(project_root, ".venv", "Scripts", "python.exe")
    if os.path.exists(venv_exe):
        python_exe = venv_exe
        print(f"Using virtual environment: {python_exe}")

    # Ensure reports directory exists
    if not os.path.exists("reports"):
        os.makedirs("reports")

    # Construct pytest command
    cmd = [python_exe, "-m", "pytest"]
    
    # Browser and Headless options (passed to conftest.py)
    cmd.append(f"--browser={args.browser}")
    cmd.append(f"--headless={'true' if args.headless else 'false'}")
    
    # Reruns
    if args.reruns > 0:
        cmd.append(f"--reruns={args.reruns}")
        
    # Parallel execution
    if args.parallel:
        cmd.append("-n")
        cmd.append("auto")
        
    # Markers (Smoke vs All)
    if args.smoke:
        cmd.append("-m")
        cmd.append("smoke")
        
    # Report
    if args.report:
        report_path = os.path.join("reports", "report.html")
        cmd.append(f"--html={report_path}")
        cmd.append("--self-contained-html")

    print(f"Running command: {' '.join(cmd)}")
    
    try:
        # Run pytest and pipe output directly to terminal
        result = subprocess.run(cmd, check=False)
        sys.exit(result.returncode)
    except FileNotFoundError:
        print("Error: 'pytest' not found. Please install requirements: pip install -r requirements.txt")
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
