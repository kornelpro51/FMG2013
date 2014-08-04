#web: gunicorn -k gevent --worker-class socketio.sgunicorn.GeventSocketIOWorker fetchmyguest.wsgi:application
web: python manage.py run_gunicorn -b 0.0.0.0:$PORT -w 9 -k gevent --max-requests 250 --preload
#web: gunicorn  fetchmyguest.wsgi:application
worker: python manage.py celeryd  --loglevel=INFO -E --concurrency=5