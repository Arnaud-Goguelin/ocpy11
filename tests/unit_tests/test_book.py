import server
from unittest.mock import patch, MagicMock


# client is def in conftest.py and inject automatically
# by pytest to all test functions
# so no need to import it here


class TestBookEndpoint:

    # mock functions to get data from json files
    @patch("server.loadCompetitions")
    @patch("server.loadClubs")
    def test_book_in_past(
        self,
        load_competitions_mock: MagicMock,
        load_clubs_mock: MagicMock,
        client,
    ):
        """
        Test if book in pasted competition is not allowed.
        """
        # mock results of functions in patch decorator
        # set up
        load_competitions_mock.return_value = [
            {
                "name": "Test Competition",
                "date": "2021-07-03 10:00:00",
                "numberOfPlaces": 10,
            }
        ]
        load_clubs_mock.return_value = [
            {
                "name": "Test Club",
                "points": 5,
            }
        ]
        # set mocked results to var used in endpoints
        server.competitions = load_competitions_mock()
        server.clubs = load_clubs_mock()

        # test
        response = client.get("/book/Test Competition/Test Club")

        assert response.status_code == 200
        assert "Too late, competition already started!" in response.data.decode()
        load_competitions_mock.assert_called_once()
        load_clubs_mock.assert_called_once()

    @patch("server.loadCompetitions")
    @patch("server.loadClubs")
    def test_book_in_futur(
        self,
        load_competitions_mock: MagicMock,
        load_clubs_mock: MagicMock,
        client,
    ):
        """
        Test if book in futur competition is allowed.
        """
        # mock results of functions in patch decorator
        # set up
        load_competitions_mock.return_value = [
            {
                "name": "Test Competition",
                "date": "2030-07-03 10:00:00",
                "numberOfPlaces": 10,
            }
        ]
        load_clubs_mock.return_value = [
            {
                "name": "Test Club",
                "points": 5,
            }
        ]
        # set mocked results to var used in endpoints
        server.competitions = load_competitions_mock()
        server.clubs = load_clubs_mock()

        # test
        response = client.get("/book/Test Competition/Test Club")

        assert response.status_code == 200
        assert "Booking for Test Competition" in response.data.decode()
        load_competitions_mock.assert_called_once()
        load_clubs_mock.assert_called_once()
