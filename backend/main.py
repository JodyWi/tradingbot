# import os

# from backend.app.main import app


# if __name__ == "__main__":
#     port = int(os.getenv("AUTOLUNO_PYTHON_PORT") or os.getenv("PORT") or "8001")
#     app.run(host="0.0.0.0", port=port, debug=True)


# backend/main.py

from backend.app.main import create_app

app = create_app()
