import server
from unittest.mock import patch, MagicMock


# client is def in conftest.py and inject automatically
# by pytest to all test functions
# so no need to import it here


class TestPurchasePlacesEndpoint:

    # mock functions to get data from json files
    @patch("server.loadCompetitions")
    @patch("server.loadClubs")
    def test_purchase_possible(
        self,
        load_competitions_mock: MagicMock,
        load_clubs_mock: MagicMock,
        client,
    ):
        """
        Test if a purchase is possible.
        """
        # mock results of functions in patch decorator
        # set up
        load_competitions_mock.return_value = [
            {
                "name": "Test Competition",
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
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": "Test Competition",
                "club": "Test Club",
                "places": 2,
            },
        )

        assert response.status_code == 200
        assert "Great-booking complete!" in response.data.decode()
        load_competitions_mock.assert_called_once()
        load_clubs_mock.assert_called_once()

    @patch("server.loadCompetitions")
    @patch("server.loadClubs")
    def test_overbooking(
        self,
        load_competitions_mock: MagicMock,
        load_clubs_mock: MagicMock,
        client,
    ):
        """
        Test if overbooking is detected.
        """

        # set up
        load_competitions_mock.return_value = [
            {
                "name": "Test Competition",
                "numberOfPlaces": 2,
            }
        ]
        load_clubs_mock.return_value = [
            {
                "name": "Test Club",
                "points": 8,
            }
        ]
        server.competitions = load_competitions_mock()
        server.clubs = load_clubs_mock()

        # test
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": "Test Competition",
                "club": "Test Club",
                "places": 8,
            },
        )

        assert response.status_code == 200
        assert "Not enough places available!" in response.data.decode()
        load_competitions_mock.assert_called_once()
        load_clubs_mock.assert_called_once()

    @patch("server.loadCompetitions")
    @patch("server.loadClubs")
    def test_book_more_than_12_places(
        self,
        load_competitions_mock: MagicMock,
        load_clubs_mock: MagicMock,
        client,
    ):
        """
        Test if booking more than 12 places is detected.
        """

        # set up
        load_competitions_mock.return_value = [
            {
                "name": "Test Competition",
                "numberOfPlaces": 20,
            }
        ]
        load_clubs_mock.return_value = [
            {
                "name": "Test Club",
                "points": 8,
            }
        ]
        server.competitions = load_competitions_mock()
        server.clubs = load_clubs_mock()

        # test
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": "Test Competition",
                "club": "Test Club",
                "places": 13,
            },
        )

        assert response.status_code == 200
        assert "Not allow to book more than 12 places." in response.data.decode()
        load_competitions_mock.assert_called_once()
        load_clubs_mock.assert_called_once()

    @patch("server.loadCompetitions")
    @patch("server.loadClubs")
    def test_club_point_deducted(
        self,
        load_competitions_mock: MagicMock,
        load_clubs_mock: MagicMock,
        client,
    ):
        """
        Test if booking more than 12 places is detected.
        """

        # set up
        load_competitions_mock.return_value = [
            {
                "name": "Test Competition",
                "numberOfPlaces": 10,
            }
        ]
        load_clubs_mock.return_value = [
            {
                "name": "Test Club",
                "points": 8,
            }
        ]
        server.competitions = load_competitions_mock()
        server.clubs = load_clubs_mock()

        test_competition = server.competitions[0]

        # test
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": "Test Competition",
                "club": "Test Club",
                "places": 5,
            },
        )

        assert response.status_code == 200
        assert test_competition["numberOfPlaces"] == 5
        load_competitions_mock.assert_called_once()
        load_clubs_mock.assert_called_once()

    @patch("server.loadCompetitions")
    @patch("server.loadClubs")
    def test_boork_more_than_club_point(
        self,
        load_competitions_mock: MagicMock,
        load_clubs_mock: MagicMock,
        client,
    ):
        """
        Test if booking more than club points is not allowed.
        """
        # set up
        load_competitions_mock.return_value = [
            {
                "name": "Test Competition",
                "numberOfPlaces": 10,
            }
        ]
        load_clubs_mock.return_value = [
            {
                "name": "Test Club",
                "points": 5,
            }
        ]
        server.competitions = load_competitions_mock()
        server.clubs = load_clubs_mock()

        # test
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": "Test Competition",
                "club": "Test Club",
                "places": 6,
            },
        )

        assert response.status_code == 200
        assert "Not enough points available." in response.data.decode()
        load_competitions_mock.assert_called_once()
        load_clubs_mock.assert_called_once()
