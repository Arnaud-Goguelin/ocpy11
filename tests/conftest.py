import pytest
from server import app

# from unittest.mock import patch


# create a test client to simulate HTTP requests without running the server
@pytest.fixture
def client():
    app.config["TESTING"] = True
    # with keyword allow us to use the simulated app in the test
    # and automatically close it when the test is done and reset state
    with app.test_client() as client:
        yield client


def create_competition_test(
    name: str = "Competition Test",
    date: str = "2021-07-03 10:00:00",
    numberOfPlaces: str = "10",
) -> dict:
    return [
        {
            "name": name,
            "date": date,
            "numberOfPlaces": numberOfPlaces,
        }
    ]


def create_club_test(
    name: str = "Club Test",
    points: str = "4",
    email: str = "test@email.com",
) -> dict:
    return [
        {
            "name": name,
            "email": email,
            "points": points,
        }
    ]


# Tip:  ORM better to use FactoryBoy: https://factoryboy.readthedocs.io/en/stable/orms.html
#  in order to create automatically test data (and classes from models in DB)

# Example to mock functions in server.py
# yet we can simply use a decorator un the test function for the same purpose
# like this: @patch("server.loadCompetitions")

# @pytest.fixture
# def mock_load_competitions(mocker):
#     return mocker.patch("server.loadCompetitions")

# @pytest.fixture
# def mock_load_clubs(mocker):
#     return mocker.patch("server.loadClubs")
