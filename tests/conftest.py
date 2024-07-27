import pytest
import os
from app.models import Fan
from app import create_app

@pytest.fixture(scope='module')
def new_fan():
    fan = Fan()
    return fan

@pytest.fixture(scope='module')
def test_client():
    # Set the testing config prior to creating app
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    app = create_app()
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client





# import pytest
# import random
# from sqlalchemy import create_engine
# from sqlalchemy.exc import OperationalError as SQLAlchemyOperationalError
# from sqlalchemy.pool import StaticPool
# from app import create_app
# from app import db


# def pytest_addoption(parser):
#     parser.addoption(
#         "--dburl",  # For SQLITE "sqlite:///.app_test.db"
#         action="store",
#         default="sqlite:///:memory:",  # Default uses SQLite in-memory database
#         help="Database URL to use for tests.",
#     )


# @pytest.fixture(scope="session")
# def db_url(request):
#     """Fixture to retrieve the database URL."""
#     return request.config.getoption("--dburl")


# @pytest.hookimpl(tryfirst=True)
# def pytest_sessionstart(session):
#     db_url = session.config.getoption("--dburl")
#     try:
#         # Attempt to create an engine and connect to the database.
#         engine = create_engine(
#             db_url,
#             poolclass=StaticPool,
#         )
#         connection = engine.connect()
#         connection.close()  # Close the connection right after a successful connect.
#         print("Using Database URL:", db_url)
#         print("Database connection successful.....")
#     except SQLAlchemyOperationalError as e:
#         print(f"Failed to connect to the database at {db_url}: {e}")
#         pytest.exit(
#             "Stopping tests because database connection could not be established."
#         )


# @pytest.fixture(scope="session")
# def app(db_url):
#     """Session-wide test 'app' fixture."""
#     test_config = {
#         "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
#         "SQLALCHEMY_TRACK_MODIFICATIONS": False,
#         "SECRET_KEY": 'Oh-so-secret-test-key',
#         "INTERVAL_TASK_ID": 'interval-task-id',
#         "SCHEDULER_API_ENABLED": False
#     }
#     app = create_app(test_config)

#     with app.app_context():
#         db.create_all()
#         yield app

#         # Close the database session and drop all tables after the session
#         db.session.remove()
#         db.drop_all()


# @pytest.fixture
# def test_client(app):
#     """Test client for the app."""
#     return app.test_client()


# @pytest.fixture
# def user_payload():
#     suffix = random.randint(1, 100)
#     return {
#         "username": f"JohnDoe_{suffix}",
#         "email": f"john_{suffix}@doe.com",
#     }
