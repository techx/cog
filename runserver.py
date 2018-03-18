from hardwarecheckout import app, socketio
import sys

if __name__ == '__main__':
    try:
        port = int(sys.argv[1]) 
    except (IndexError, ValueError):
        port = 5000
    socketio.run(app, host='0.0.0.0', port=port)
