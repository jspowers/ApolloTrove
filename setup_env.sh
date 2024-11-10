# Step 1: Create virtual environment
python3 -m venv venv

# Step 2: Activate virtual environment
# TODO: Bug this isn't working?
source venv/bin/activate

# Step 3: Install dependencies from requirements.txt
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo "requirements.txt not found"
    exit
fi

# Step 4: Export current working directory to the PythonPath variable
# TODO: bug this isn't working because the Venv Activation is being skipped for some reason
# export PYTHONPATH=pwd

echo "Setup complete. Virtual environment created and dependencies installed."