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
```
{
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

### Replay data
Look at `test/Reforged1Pretty.json` and `test/Reforged2Pretty.json` for a human readable glance of the parsed format.

### CSS
Since we're writing styles in SCSS, whenever changes are made we'll need to compile the SCSS to plain CSS. `pip install libsass` gives you the library you need to run `build.py` in `/perchweb/static/scss/`.

## Production deployment
* ssh to production server
* `sudo -u www-data git pull`
* `systemctl restart highperch`

Some updates will change the formats of the SQLite `.db`s and/or `replaydata/.json`s, manual update script will be provided.

## Production environment

This goes in a systemd unit, e.g. `/etc/systemd/system/highperch.service`:

```
[Unit]
Description=Gunicorn WSGI for the Highperch Flask app
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/highper.ch/perchweb
Environment="PATH=/var/www/highper.ch/env/bin://usr/bin/"
EnvironmentFile=/etc/nginx/highperch-envvars
ExecStart=/var/www/highper.ch/env/bin/gunicorn --workers 4 --log-file /var/log/nginx/gunicorn/highperch.log --log-level DEBUG --bind unix:../highperch.sock app:app

[Install]
WantedBy=multi-user.target
```

The EnvironmentFile from the unit above needs to contain these lines:
```
SERVER_HOST=localhost
SERVER_PORT=5000
HIGHPERCH_ENVIRONMENT=production
HIGHPERCH_FLASK_KEY=(it's a secret)
HIGHPERCH_ADMIN_HASH=(it's a secret)
```

The stream poller gets called with this cron job, run as `www-data`:

```
*/1 * * * * /usr/bin/env bash -c 'source /etc/nginx/streampoll-envvars && source /var/www/highper.ch/env/bin/activate && python /var/www/highper.ch/streampoller.py'
```

The envvar file from the above needs to contain these lines:

```
export HIGHPERCH_STREAM_WEBHOOK=(it's a secret)
export HIGHPERCH_TWITCH_CLIENT_ID=(it's a secret)
```
