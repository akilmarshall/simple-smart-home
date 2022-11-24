test: web.py
	hug -f web.py

uwsgi: web.py
	uwsgi --http 0.0.0.0:80 --wsgi-file web.py --callable __hug_wsgi__
