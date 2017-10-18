rm intern.db
sqlite3 intern.db < intern.schema
gunicorn --reload --log-level debug --worker-class eventlet -w 1 interns:app --bind 0.0.0.0:8000
