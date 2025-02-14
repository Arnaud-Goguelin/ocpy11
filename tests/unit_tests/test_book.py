from tests.conftest import create_one_club_test, create_one_competition_test
from unittest.mock import patch


# client is def in conftest.py and inject automatically
# by pytest to all test functions
# so no need to import it here


class TestBookEndpoint:

    # mock data from json files
    @patch("server.competitions", create_one_competition_test())
    @patch("server.clubs", create_one_club_test())
    def test_book_in_past(
        self,
        client,
    ):
        """
        Test if book in pasted competition is not allowed.
        """
        # set up already done in patch decorator

        # test
        response = client.get("/book/Competition Test/Club Test")

        assert response.status_code == 200
        assert "Too late, competition already started!" in response.data.decode()
        # load_competitions_mock.assert_called_once()
        # load_clubs_mock.assert_called_once()

    @patch(
        "server.competitions", create_one_competition_test(date="2030-07-03 10:30:00")
    )
    @patch("server.clubs", create_one_club_test())
    def test_book_in_future(
        self,
        client,
    ):
        """
        Test if book in future competition is allowed.
        """
        # set up already done in patch decorator

        # test
        response = client.get("/book/Competition Test/Club Test")

        assert response.status_code == 200
        assert "Booking for Competition Test" in response.data.decode()
