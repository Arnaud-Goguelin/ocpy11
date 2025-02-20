import server
from unittest.mock import patch, MagicMock
from tests.conftest import create_one_competition_test, create_one_club_test


@patch("server.loadClubs", return_value=create_one_club_test())
@patch(
    "server.loadCompetitions",
    return_value=create_one_competition_test(date="2030-07-03 10:30:00"),
)
def test_summary_to_welcome(
    load_clubs_mock: MagicMock,
    load_competitions_mock: MagicMock,
    client,
) -> None:
    """
    Test if flow from summary to welcome works well.
    """

    # --- set up ---
    # here, mocking data ensure we have the same data
    # and post email is not stored in data
    server.competitions = server.loadCompetitions()
    server.clubs = server.loadClubs()

    # --- test ---
    load_competitions_mock.assert_called_once()
    load_clubs_mock.assert_called_once()
    # test if the summary page is displayed according to the email received
    response = client.post("/showSummary", data={"email": "test@email.com"})
    assert response.status_code == 200
    assert "Welcome, test@email.com" in response.data.decode()
    # test if the book page is displayed according to the competition and club received
    response = client.get("/book/Competition Test/Club Test")
    assert response.status_code == 200
    assert "Booking for Competition Test" in response.data.decode()
