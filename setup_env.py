import sys
import subprocess
import os
import venv
from pathlib import Path

def setup_environment():
    base_dir = Path(__file__).parent.absolute()
    venv_dir = base_dir / "venv"
    
    print(f"Setting up environment in {venv_dir}...")
    
    # 1. Create Virtual Environment if it doesn't exist
    if not venv_dir.exists():
        print("Creating virtual environment...")
        venv.create(venv_dir, with_pip=True)
    else:
        print("Virtual environment already exists.")

    # 2. Determine python and pip paths
    if sys.platform == "win32":
        python_executable = venv_dir / "Scripts" / "python.exe"
        pip_executable = venv_dir / "Scripts" / "pip.exe"
    else:
        python_executable = venv_dir / "bin" / "python"
        pip_executable = venv_dir / "bin" / "pip"

    if not python_executable.exists():
        print(f"Error: Python executable not found at {python_executable}")
        return

    # 3. Upgrade pip
    print("Upgrading pip...")
    subprocess.check_call([str(python_executable), "-m", "pip", "install", "--upgrade", "pip"])

    # 4. Install requirements
    requirements_file = base_dir / "requirements.txt"
    if requirements_file.exists():
        print(f"Installing dependencies from {requirements_file.name}...")
        subprocess.check_call([str(pip_executable), "install", "-r", str(requirements_file)])
    else:
        print("requirements.txt not found!")

    print("\nSetup complete! You can run the application with:")
    if sys.platform == "win32":
        print(f"{venv_dir}\\Scripts\\python.exe main.py")
    else:
        print(f"{venv_dir}/bin/python main.py")

if __name__ == "__main__":
    setup_environment()
