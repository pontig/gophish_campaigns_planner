python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

pip install --upgrade urllib3 requests six

pip install --force-reinstall --no-deps gophish
pip install -U requests urllib3 six