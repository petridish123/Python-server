import os
import subprocess
import sys

def create_and_setup_venv():
    # Create venv in current working directory
    venv_dir = os.path.join(os.getcwd(), "venv")

    print(f"Creating virtual environment at {venv_dir}...")
    subprocess.check_call([sys.executable, "-m", "venv", venv_dir])

    # Determine the path to pip inside the venv
    if os.name == "nt":  # Windows
        pip_path = os.path.join(venv_dir, "Scripts", "pip.exe")
    else:
        pip_path = os.path.join(venv_dir, "bin", "pip")

    #If requirement is opened then this works
    try:
        with open("requirements.txt") as f:
            packages = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except:
        packages = ["numpy", "qasync", "PyQt6", "websockets","Shared"] 


    


    print(f"Installing packages: {', '.join(packages)}")
    subprocess.check_call([pip_path, "install", *packages])

    print("\n✅ Environment setup complete!")
    print(f"To activate it, run:\n  {venv_dir}\\Scripts\\activate" if os.name == "nt" else f"source {venv_dir}/bin/activate")

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