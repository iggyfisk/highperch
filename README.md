# highper.ch web
Replay database extraordinarie

## Dev environment
* `python --version` or `python3 --version` >= 3.5.0
* `virtualenv -h`
The `-p` option default should be your Python3 interpreter, else specify it. If virtualenv is not installed, `pip install virtualenv` or `pip3 install virtualenv`
* For replay parsing, `node --version` >= 10.0.0 (`brew install node`)
* For replay parsing, `yarn --version` >= 1.3.0 (`brew install yarn`)
* Clone this repository, cwd to repo root.
* `virtualenv env` to initialize your virtual environment
* `source env/bin/activate` or `env\Scripts\Activate` (Windows) to enter your virtual environment
* `pip install -r requirements.txt`
* For replay parsing, `yarn install`
* `python initcontent.py` (yes/yes)
* `python runserver.py`
* `http://localhost:5555/` Go!
* `deactivate` to reclaim your terminal when you're done

### Reasonable editors
* Windows: VSCode, enter your virtual environment above and `pip install pylint` `pip install autopep8` then Ctrl+Shift+P in VSCode and `Python: Select interpreter`, find your virtualenv in the list
* MacOS: Atom, doesn't pick up the external libraries. Pycharm CE, picks up virtualenv automatically

## Production deployment
Coming soon, something with nginx and uwsgi. No crazy build procedures, just a repo pull and some gitignored config files, probably hash the JS and CSS, MAYBE minify them.
