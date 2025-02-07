import server
from unittest.mock import patch, MagicMock
from tests.conftest import create_competition_test, create_club_test


# client is def in conftest.py and inject automatically
# by pytest to all test functions
# so no need to import it here


class TestShowSummaryEndpoint:

    @patch("server.loadClubs", return_value=create_club_test())
    @patch("server.loadCompetitions", return_value=create_competition_test())
    def test_unknow_email(
        self,
        load_competitions_mock: MagicMock,
        load_clubs_mock: MagicMock,
        client,
    ):
        """
        Test if unknow remail is detected.
        """
        # set up
        # here, mocking data ensure we have the same data
        # and post email is not stored in data
        server.competitions = server.loadCompetitions()
        server.clubs = server.loadClubs()

        # test
        # TODO try follow_redirect
        response = client.post("/showSummary", data={"email": "unknows@email.com"})
        # 302 is the status code for redirect
        assert response.status_code == 302
        assert "Redirecting..." in response.data.decode()

        # Follow the redirect
        redirected_response = client.get(response.headers["Location"])
        assert "Email not registered." in redirected_response.data.decode()
        load_competitions_mock.assert_called_once()
        load_clubs_mock.assert_called_once()
