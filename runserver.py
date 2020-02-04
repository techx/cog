from cog import app# , socketio
from initialize import rebuild 
import sys
import os

if __name__ == '__main__':
    if os.getenv('ENV', '') == 'test':
        rebuild()
    port = int(os.getenv("FLASK_RUN_PORT", "80"))
    debug = os.getenv("FLASK_DEBUG") == "1"
    app.run(host='0.0.0.0', port=port, debug=debug)
