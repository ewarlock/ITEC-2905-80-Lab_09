from selenium.webdriver.firefox.webdriver import WebDriver

from django.test import LiveServerTestCase


class TitleTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass() # running setupclass
        cls.selenium = WebDriver()
        cls.selenium.implicity_wait(10) # wait up to ten seconds for something to happen


    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super.tearDownClass()

    def test_title_on_home_page(self):

        self.selenium.get(self.live_server_url) # reference live server
        self.assertIn('Travel Wishlist', self.selenium.title)


# python manage.py test travel_wishlist.functional_tests

# I have not been able to get this to work
"""ERROR: setUpClass (travel_wishlist.functional_tests.TitleTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\edwin\Documents\Capstone\Lab_09\wishlist\travel_wishlist\functional_tests.py", line 11, in setUpClass
    cls.selenium = WebDriver()
  File "C:\Users\edwin\Documents\Capstone\Lab_09\env\lib\site-packages\selenium\webdriver\firefox\webdriver.py", line 180, in __init__
    RemoteWebDriver.__init__(
  File "C:\Users\edwin\Documents\Capstone\Lab_09\env\lib\site-packages\selenium\webdriver\remote\webdriver.py", line 266, in __init__
    self.start_session(capabilities, browser_profile)
  File "C:\Users\edwin\Documents\Capstone\Lab_09\env\lib\site-packages\selenium\webdriver\remote\webdriver.py", line 357, in start_session
    response = self.execute(Command.NEW_SESSION, parameters)
  File "C:\Users\edwin\Documents\Capstone\Lab_09\env\lib\site-packages\selenium\webdriver\remote\webdriver.py", line 418, in execute
    self.error_handler.check_response(response)
  File "C:\Users\edwin\Documents\Capstone\Lab_09\env\lib\site-packages\selenium\webdriver\remote\errorhandler.py", line 243, in check_response
    raise exception_class(message, screen, stacktrace)
selenium.common.exceptions.SessionNotCreatedException: Message: Expected browser binary location, but unable to find binary in default location, no 'moz:firefoxOptions.binary' capability provided, and no binary flag set on the command line"""