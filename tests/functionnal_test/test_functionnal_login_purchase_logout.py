import time
import pytest
from urllib.parse import quote
from selenium import webdriver

from server import clubs, competitions

@pytest.mark.functional
class TestFunctional:
    _base_url = "127.0.0.1:5000"
    _iron_temple = clubs[1]
    _future_competition = competitions[-1]

    def test_login_book_places_logout(self):
        """
        Test the login, book places and logout functionality
        """
        # set up the browser
        driver = webdriver.Firefox()
        # open the browser and go to the website
        driver.get(f"http://{self._base_url}")
        # wait and check if the landing page is correct
        time.sleep(1)
        assert "Welcome to the GUDLFT Registration Portal!" in driver.page_source

        # enter email and click on the login button
        email_input = driver.find_element("name", "email")
        email_input.send_keys(self._iron_temple["email"])

        submit_button = driver.find_element("tag name", "button")
        submit_button.click()
        time.sleep(1)
        assert f" Points available: {self._iron_temple["points"]}" in driver.page_source

        # select competition
        # create link to follow to select the chosen competition
        # need to encode the link to avoid issues with special characters and spaces
        link_value = f"/book/{self._future_competition['name']}/{self._iron_temple['name']}"
        encoded_link = quote(link_value)
        link_to_book_places = driver.find_element("xpath", f"//a[@href='{encoded_link}']")
        link_to_book_places.click()
        time.sleep(1)
        assert f"Places available: {self._future_competition["numberOfPlaces"]}" in driver.page_source
        
        # book places
        places_input = driver.find_element("name", "places")
        places_input.send_keys("2")
        submit_button = driver.find_element("tag name", "button")
        submit_button.click()
        updated_club_points = int(self._iron_temple["points"]) - 2
        updated_competition_places = int(self._future_competition["numberOfPlaces"]) - 2
        time.sleep(1)
        assert "Great-booking complete!" in driver.page_source
        assert updated_club_points == 2
        assert updated_competition_places == 38

        # logout
        link_to_logout = driver.find_element("xpath", "//a[@href='/logout']")
        link_to_logout.click()
        time.sleep(1)
        assert "Welcome to the GUDLFT Registration Portal!" in driver.page_source
        
        # quit the browser
        driver.quit()
