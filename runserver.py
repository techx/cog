from cog import app, socketio
from initialize import rebuild 
import sys
import os

if __name__ == '__main__':
    if os.environ['ENV'] == 'test':
        rebuild()
    try:
        port = int(sys.argv[1]) 
    except (IndexError, ValueError):
        port = 80
    socketio.run(app, host='0.0.0.0', port=port)
