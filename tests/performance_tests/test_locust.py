from locust import HttpUser, task
from server import clubs, competitions


class PerfTests(HttpUser):

    _users_number = 6
    _registered_club = clubs[1]

    @task(_users_number)
    def test_get_index(self):
        self.client.get("/")

    @task(_users_number)
    def test_post_showSummary(self):
        self.client.post("/showSummary", {"email": self._registered_club["email"]})

    @task(_users_number)
    def test_post_purchasePlaces(self):
        self.client.post(
            "/purchasePlaces",
            {
                "competition": competitions[-1]["name"],
                "club": self._registered_club["name"],
                "places": 2,
            },
        )
