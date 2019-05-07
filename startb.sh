python3 -m venv venvnasza \
&& source venvnasza/bin/activate \
&& pip install -r requirements.txt \
&& export FLASK_ENV=development \
&& flask run
