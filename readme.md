Prerequirements: Python 3+ with pip

Steps to run a local debug mode version:
1. Go to the main directory of the project on your local drive
2. Create a Python virtualenv: `python -m venv venvnasza`
3. Activate the venv: on MAC `source venvnasza/bin/activate`
4. Install all the required modules: `pip install -r requirements.txt`
5.1 In command line write `export FLASK_ENV=development` for dev env only
5. Run the app locally: `flask run`
6. App will be running on `127.0.0.1:5000` <- that's the "main address"

Or a shortcut: 
1. Run `sh startb.sh`

To run frontend: 
1. Make sure you have Node.js installed version 8+
2. go to 'frontend' folder
3. Install packages `npm install` or `yarn` if you have yarn.
4. Run server with `npm run dev` or `yarn dev`.
