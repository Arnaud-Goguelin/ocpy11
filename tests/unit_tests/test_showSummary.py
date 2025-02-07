# client is def in conftest.py and inject automatically
# by pytest to all test functions
# so no need to import it here


class TestShowSummaryEndpoint:

    def test_unknow_email(
        self,
        client,
    ):
        """
        Test if unknow remail is detected.
        """
        # set up
        # no set up here as we want to try an unknown email

        # test
        response = client.post("/showSummary", data={"email": "unknown@email.com"})
        # 302 is the status code for redirect
        assert response.status_code == 302
        assert "Redirecting..." in response.data.decode()

        # Follow the redirect
        response = client.get(response.headers["Location"])
        assert "Email not registered." in response.data.decode()
