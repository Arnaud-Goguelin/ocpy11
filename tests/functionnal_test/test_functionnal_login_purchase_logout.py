import pytest
from urllib.parse import quote
from selenium import webdriver

from server import clubs, competitions

# TODO: try to adapt functional test to updated data and not only data when app is started


@pytest.mark.functional
class TestFunctional:
    _base_url = "127.0.0.1:5000"
    _iron_temple = clubs[1]
    _future_competition = competitions[-1]
    _places_booked = 2

    def test_login_book_places_logout(self):
        """
        Test the login, book places and logout functionality
        """
        try:
            # set up the browser
            driver = webdriver.Firefox()
            # open the browser and go to the website
            driver.get(f"http://{self._base_url}")
            # check if the landing page is correct
            assert "Welcome to the GUDLFT Registration Portal!" in driver.page_source

            # enter email and click on the login button
            email_input = driver.find_element("name", "email")
            email_input.send_keys(self._iron_temple["email"])

            submit_button = driver.find_element("tag name", "button")
            submit_button.click()
            assert (
                f" Points available: {self._iron_temple["points"]}"
                in driver.page_source
            )

            # select competition
            # create link to follow to select the chosen competition
            # need to encode the link to avoid issues with special characters and spaces
            link_value = (
                f"/book/{self._future_competition['name']}/{self._iron_temple['name']}"
            )
            encoded_link = quote(link_value)
            link_to_book_places = driver.find_element(
                "xpath", f"//a[@href='{encoded_link}']"
            )
            link_to_book_places.click()
            assert (
                f"Places available: {self._future_competition["numberOfPlaces"]}"
                in driver.page_source
            )

            # book places
            places_input = driver.find_element("name", "places")
            places_input.send_keys(str(self._places_booked))
            submit_button = driver.find_element("tag name", "button")
            submit_button.click()
            self._iron_temple["points"] = (
                int(self._iron_temple["points"]) - self._places_booked
            )
            self._future_competition["numberOfPlaces"] = (
                int(self._future_competition["numberOfPlaces"]) - self._places_booked
            )
            assert "Great-booking complete!" in driver.page_source
            assert (
                f"Points available: {self._iron_temple["points"]}" in driver.page_source
            )
            assert (
                f"Number of Places: {self._future_competition["numberOfPlaces"]}"
                in driver.page_source
            )

            # logout
            link_to_logout = driver.find_element("xpath", "//a[@href='/logout']")
            link_to_logout.click()
            assert "Welcome to the GUDLFT Registration Portal!" in driver.page_source

        finally:
            # quit the browser
            driver.close()
