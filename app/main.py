import signal
import sys
from server import create_server
from config import Config

def main():
    app = create_server()
    config = Config()

    def shutdown_handler(signal_received, frame):
        print("Shutting down gracefully...")
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    print(f"Starting server on port {config.HTTP_PORT}...")
    app.run(host="0.0.0.0", port=config.HTTP_PORT)

if __name__ == "__main__":
    main()