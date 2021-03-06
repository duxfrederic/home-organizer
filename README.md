# home-organizer
A small flask-bootstrap app to help with holding an inventory. 
## Deployment 
Start by creating an environment to run this and installing the dependencies:
```bash
$ git clone git@github.com:duxfrederic/home-organizer.git
$ cd home-organizer
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Then, you might want to modify `app/models.py` to include your own "buildings" and "stories". Finally, initialize the database:
```bash
$ flask db init
$ flask db migrate -m "creation of the database"
$ flask db upgrade
```
One more thing, create the directories that will contain the pictures:
```bash
$ mkdir -p app/static/locations_pictures app/static/items_pictures
```

You can now run the development version with `flask run`. For production, use e.g. `gunicorn`:
```bash
$ pip install gunicorn
$ gunicorn -b 0.0.0.0:5000 -w 2 app:app
```
This can be easily made to start automatically with e.g. `systemctl`. A reverse proxy will be useful if you want the app to be accessible on a certain site on the usual http or https ports. (Or you can simply run gunicorn on port 80.)

## Backup
You only need to backup `app.db`, `app/static/locations_pictures` and `app/static/items_pictures`. 
