import server
from unittest.mock import patch, MagicMock
from tests.conftest import create_one_competition_test, create_one_club_test


# client is def in conftest.py and inject automatically
# by pytest to all test functions
# so no need to import it here


class TestPurchasePlacesEndpoint:

    # mock functions to get data from json files
    # ! becareful of the order of patching
    # ! the closest to the test is the first to be patched
    @patch("server.loadClubs", return_value=create_one_club_test())
    @patch("server.loadCompetitions", return_value=create_one_competition_test())
    def test_purchase_possible(
        self,
        load_competitions_mock: MagicMock,
        load_clubs_mock: MagicMock,
        client,
    ):
        """
        Test if a purchase is possible.
        """

        # set up
        # force loading data, mocked data will be used this way
        server.competitions = server.loadCompetitions()
        server.clubs = server.loadClubs()

        competition_test = server.competitions[0]
        club_test = server.clubs[0]

        # test
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": competition_test["name"],
                "club": club_test["name"],
                "places": 2,
            },
        )

        assert response.status_code == 200
        assert "Great-booking complete!" in response.data.decode()
        load_competitions_mock.assert_called_once()
        load_clubs_mock.assert_called_once()

    @patch("server.loadClubs", return_value=create_one_club_test())
    @patch(
        "server.loadCompetitions",
        return_value=create_one_competition_test(numberOfPlaces="2"),
    )
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
        # force loading data, mocked data will be used this way
        server.competitions = server.loadCompetitions()
        server.clubs = server.loadClubs()

        competition_test = server.competitions[0]
        club_test = server.clubs[0]

        # test
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": competition_test["name"],
                "club": club_test["name"],
                "places": 8,
            },
        )

        assert response.status_code == 200
        assert "Not enough places available!" in response.data.decode()
        load_competitions_mock.assert_called_once()
        load_clubs_mock.assert_called_once()

    @patch("server.loadClubs", return_value=create_one_club_test(points="15"))
    @patch(
        "server.loadCompetitions",
        return_value=create_one_competition_test(numberOfPlaces="20"),
    )
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
        # force loading data, mocked data will be used this way
        server.competitions = server.loadCompetitions()
        server.clubs = server.loadClubs()

        competition_test = server.competitions[0]
        club_test = server.clubs[0]

        # test
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": competition_test["name"],
                "club": club_test["name"],
                "places": 13,
            },
        )

        assert response.status_code == 200
        assert "Not allow to book more than 12 places." in response.data.decode()
        load_competitions_mock.assert_called_once()
        load_clubs_mock.assert_called_once()

    @patch("server.loadClubs", return_value=create_one_club_test(points="10"))
    @patch("server.loadCompetitions", return_value=create_one_competition_test())
    def test_club_point_deducted(
        self,
        load_competitions_mock: MagicMock,
        load_clubs_mock: MagicMock,
        client,
    ):
        """
        Test if clubs's points are deducted after booking.
        """

        # set up
        # force loading data, mocked data will be used this way
        server.competitions = server.loadCompetitions()
        server.clubs = server.loadClubs()

        competition_test = server.competitions[0]
        club_test = server.clubs[0]

        # test
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": competition_test["name"],
                "club": club_test["name"],
                "places": 5,
            },
        )

        assert response.status_code == 200
        assert club_test["points"] == 5
        load_competitions_mock.assert_called_once()
        load_clubs_mock.assert_called_once()

    @patch("server.loadClubs", return_value=create_one_club_test(points="5"))
    @patch("server.loadCompetitions", return_value=create_one_competition_test())
    def test_book_more_than_club_point(
        self,
        load_competitions_mock: MagicMock,
        load_clubs_mock: MagicMock,
        client,
    ):
        """
        Test if booking more than club points is not allowed.
        """
        # set up
        # force loading data, mocked data will be used this way
        server.competitions = server.loadCompetitions()
        server.clubs = server.loadClubs()

        competition_test = server.competitions[0]
        club_test = server.clubs[0]

        # test
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": competition_test["name"],
                "club": club_test["name"],
                "places": 6,
            },
        )

        assert response.status_code == 200
        assert "Not enough points available." in response.data.decode()
        load_competitions_mock.assert_called_once()
        load_clubs_mock.assert_called_once()
