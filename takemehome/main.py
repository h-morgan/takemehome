from takemehome.ui import run_app
from takemehome.database import init_db

if __name__ == "__main__":
    # Initialize the database
    init_db()

    # Run the application
    run_app()
