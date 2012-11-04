web: python src/manage.py collectstatic --noinput; python src/manage.py run_gunicorn server.wsgi -b 0.0.0.0:$PORT --workers=4
