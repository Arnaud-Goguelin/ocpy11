### Main objective
This project is an exercise to learn how to test an app.
The app is an 'MVP' to book places in a competitions for sports clubs.
An email is needed to log in and book places.
It is only possible to book a maximum of 12 places per competitions.


### How to install project
To install the project, follow these steps:
1. Clone the repository:
```
git clone https://github.com/Arnaud-Goguelin/ocpy11.git
cd your-repo
```
2. Set up your virtual environment:
```
python3 -m venv my_virutal_env
# on Linux
source my_virtual_env/bin/activate
# on Windows
my_virtual_env\Scripts\activate
```
3. Install the requirements
```
pip install -r requirements.txt
```
4. Run the app
```
# debug is set to True
python server.py
```

### Configurations
Python Version: This project uses Python 3.12.
Flask: The web framework used for this application.
Database: JSON files for this MVP (restart app to reset DB).

### To execute tests
To run tests, use these commands:
```
pytest .
# to  execute unit and integration tests only
pytest --ignore=tests/functional_tests --ignore=tests/performance_tests
```

### External Sources

- Flask Documentation: [Flask Docs](https://flask.palletsprojects.com/en/stable/)
- Pytest Documentation: [Pytest Docs](https://docs.pytest.org/en/stable/)
- Selenium Documentation: [Selenium Docs](https://selenium-python.readthedocs.io/getting-started.html)
- Locust Documentation: [Locust Docs](https://docs.locust.io/en/stable/)
- Other Libraries: other libraries are also used in this app,
but the most important, according to the objective, are already listed.
