# JukePi

Web media server built using python, flask and sqlalchemy. 
Point to your media folder to browse and play anything on that folder from a simple web UI.

## Installation

~~~
pip install -r requirements.txt
~~~

## Run
Make sure to provide the appropriate configuration file in the `resources` folder as per the template provided.
To create the database file `library.db`, you need to run:
~~~
python library_updater.py
~~~
Next you can spin up the server by running 
~~~
python -m jukepi.ui.server
~~~

## Run Dockerized
Build & Run the images:
~~~
docker-compose build
docker-compose up -d
~~~

## TODO
* Separate and dockerize db manager
* Implement queue:
    * server-side
    * ui
* lastfm, musicbrainz integration:
    * scrobbling
    * text
    * cover images
    