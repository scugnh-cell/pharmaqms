import os
import sys

# Ensure backend dir is on sys.path for config import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

app = create_app()

if __name__ == "__main__":
    port = 8889
    env = os.environ.get("FLASK_ENV", "production")

    if env == "development":
        print(f"PharmaQMS [DEV] running at http://localhost:{port}")
        app.run(host="127.0.0.1", port=port, debug=True)
    else:
        from waitress import serve
        print(f"PharmaQMS running at http://localhost:{port}")
        serve(app, host="127.0.0.1", port=port)
