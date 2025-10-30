import os
import subprocess
import sys
import shutil

def find_system_python():
    """Try to locate a system Python executable."""
    candidates = ["python", "python3", r"C:\Python39\python.exe"]
    for candidate in candidates:
        try:
            subprocess.check_call([candidate, "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return candidate
        except Exception:
            continue
    sys.exit("❌ Could not find a system Python installation.")
def create_and_setup_venv():
    # Create venv in current working directory
    venv_dir = os.path.join(os.getcwd(), "venv")

    print(f"Creating virtual environment at {venv_dir}...")


        # If running as a PyInstaller .exe, sys.frozen is True
    if getattr(sys, 'frozen', False):
        python_exec = find_system_python()
    else:
        python_exec = sys.executable

    subprocess.check_call([python_exec, "-m", "venv", venv_dir])
    # subprocess.check_call([sys.executable, "-m", "venv", venv_dir])

    # Determine the path to pip inside the venv
    if os.name == "nt":  # Windows
        pip_path = os.path.join(venv_dir, "Scripts", "pip.exe")
    else:
        pip_path = os.path.join(venv_dir, "bin", "pip")

    #If requirement is opened then this works
    # try:
    #     with open("requirements.txt") as f:
    #         packages = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    # except:
    packages = ["numpy", "qasync", "PyQt6", "websockets"]# I wanted shared but this won't get the right one,"Shared"] 


    


    print(f"Installing packages: {', '.join(packages)}")
    subprocess.check_call([pip_path, "install", *packages])

    print("\n✅ Environment setup complete!")
    print(f"To activate it, run:\n  {venv_dir}\\Scripts\\activate" if os.name == "nt" else f"source {venv_dir}/bin/activate")

    open_activated_shell(venv_dir)

def open_activated_shell(venv_dir):
    """Opens a terminal with the venv activated."""
    print("Opening an activated shell...")

    if os.name == "nt":  # Windows
        activate_cmd = os.path.join(venv_dir, "Scripts", "activate.bat")
        # Launch cmd with venv activated, then stay open
        subprocess.call(["cmd.exe", "/k", activate_cmd])
    else:  # macOS/Linux
        activate_cmd = os.path.join(venv_dir, "bin", "activate")
        subprocess.call(["bash", "--rcfile", activate_cmd])

if __name__ == "__main__":
    create_and_setup_venv()


"""
This will be used to make the py installer
executable.
This will be run before
any client uses the qtwebsocket
to correctly create a venv
and install the following packages
also found in requirements.txt
numpy
Shared
PyQt6
websockets
qasync

"""


"""
directory should look like this:
root-
    \- py_builder.exe
    \- Shared-
             \- __init__.py   
    \- Requirements.txt   
    \- qtwebsocket.py

"""

"""
What I want this to do now...

I want this to make a folder/package with a readme.md
a requirements.txt
and the client and the Shared package

The readme will detail that you need to run pip from inside that directory using -r requirements.txt after creating a venv

"""