# highper.ch web
Replay database extraordinarie

## Dev environment
* `python --version` or `python3 --version` >= 3.5.0
* `virtualenv -h`
The `-p` option default should be your Python3 interpreter, else specify it. If virtualenv is not installed, `pip install virtualenv` or `pip3 install virtualenv`

* Clone this repository, cwd to repo root.
* `virtualenv env` to initialize your virtual environment
* `source env/bin/activate` or `env\Scripts\Activate` (Windows) to enter your virtual environment
* `pip install -r Requirements.txt`
* `python runserver.py`
* `http://localhost:5555/` Go!

### Reasonable editors
* Windows: VSCode, enter your virtual environment above and `pip install pylint` `pip install autopep8` then Ctrl+Shift+P in VSCode and `Python: Select interpreter`, find your virtualenv in the list
* MacOS: Pycharm CE, picks up virtualenv automatically

## Production deployment
Coming soon, something with nginx and uwsgi. No crazy build procedures, just a repo pull and some gitignored config files, probably hash the JS and CSS, MAYBE minify them.
