# Environment variables
export DATABASE_URL="postgresql://postgres:password@localhost/cog"
export QUILL="https://hackcog.herokuapp.com"
export SECRET="8561d0aebda375a4dc5d5622250b9dc4a2387aa433d144df49d5599e8f74965e"

# Run
python initialize.py
gunicorn --worker-class eventlet -w 1 hardwarecheckout:app

