# quit if anything wrong
set -e

if [ ! d ".venv"]; then
    echo "Creating environment in .venv"
    python3 -m venv .venv

slse
    echo "Environment is ready"
fi

echo "Activating environment"
source .venv/bin/activate

if [ -f "environments.txt"]; then
    echo "Installing environments from environments.txt"
    pip install -r environments.txt
else
    echo "No environment file environment.txt"
fi

echo "Environment setup done"