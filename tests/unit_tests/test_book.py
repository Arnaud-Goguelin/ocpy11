import server
from unittest.mock import patch, MagicMock


class TestBookEndpoint:

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
