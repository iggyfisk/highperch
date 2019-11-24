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
* `python perchweb/app.py`
* `http://localhost:5000/` Go!
* `deactivate` to reclaim your terminal when you're done

### Tested editors
#### VSCode
Symbols, highlighting, formatting, debugging

* Enter your virtual environment
* `pip install pylint` syntax highlighting
* `pip install autopep8` auto formatting (Shift+Alt+F / Shift+Option+F)
* Ctrl+Shift+P / Cmd+Shift+P inside VSCode, `Python: Select interpreter`, find your virtual environment in the list
* in `launch.json`:
```{
    "name": "Python: Flask",
    "type": "python",
    "request": "launch",
    "module": "flask",
    "env": {
        "FLASK_APP": "perchweb/app",
        "FLASK_ENV": "development",
        "FLASK_DEBUG": "1"
    },
    "args": [
        "run",
        "--no-reload",
        "--port",
        "5000"
    ],
    "jinja": true
},
```
This should get you Python debugging and template auto reload on change. Need manual restart for Python changes.

#### Pycharm
Symbols, highlighting, formatting, debugging. Just open the project and select your virtual environment as the interpreter when prompted

#### Atom
Highlighting. I'm sure the rest can be configured if you install enough plugins.

### Replay data
Look at `test/Reforged1Pretty.json` and `test/Reforged2Pretty.json` for a human readable glance of the parsed format.

## Production deployment
* ssh to production server
* `sudo -u www-data git pull`
* `python initcontent.py` to reset during the development phase, but don't replace the config!
* `systemctl restart highperch`

Before we go public it's `python initcontent.py` one last time. After that, data format updates will probably be more bespoke
