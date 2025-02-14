import server
from unittest.mock import patch, MagicMock
from tests.conftest import create_one_competition_test, create_one_club_test


@patch("server.loadClubs", return_value=create_one_club_test(points="10"))
@patch("server.loadCompetitions", return_value=create_one_competition_test(date="2030-07-03 10:30:00"))
def test_summary_to_welcome(
    load_clubs_mock: MagicMock,
    load_competitions_mock: MagicMock,
    client,
) -> None:
    """
    Test if flow from book to purchase works well.
    """

    # --- set up ---
    # here, mocking data ensure we have the same data
    # and post email is not stored in data
    server.competitions = server.loadCompetitions()
    server.clubs = server.loadClubs()

    competition_test = server.competitions[0]
    club_test = server.clubs[0]

    # --- test ---
    load_competitions_mock.assert_called_once()
    load_clubs_mock.assert_called_once()
    # test if the book page is displayed according to the competition and club received
    response = client.get(f"/book/{competition_test["name"]}/{club_test["name"]}")
    assert response.status_code == 200
    assert "Booking for Competition Test" in response.data.decode()

    # test if the purchase is confirmed and point deducted
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition_test["name"],
            "club": club_test["name"],
            "places": 5,
        },
    )

    assert response.status_code == 200
    assert "Great-booking complete!" in response.data.decode()
    assert club_test["points"] == 5
