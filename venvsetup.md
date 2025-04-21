# 0. Install and configure pyenv (only once)
brew install pyenv #For mac/linux
pyenv install 3.10.13
pyenv local 3.10.13

# 1. Install UV 
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env  # Enable uv in current shell

# 2. Create virtual environment - only once
uv venv 

# 3. Activate venv
source .venv/bin/activate

# 4. Install project dependencies
uv pip install --upgrade crewai
uv pip install -r requirements.txt

# 5. Run your Streamlit app
streamlit run streamlit_app.py
