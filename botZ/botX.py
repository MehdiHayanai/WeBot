from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
from selenium.webdriver.remote.webelement import WebElement
from typing import Optional
import os
import base64
from time import sleep


class BotX:
    def __init__(self, driver_name: str, url: str, time_out: int = 10) -> None:
        """
        Initialize the BotX class.

        Args:
            driver_name (str): Name of the driver.
            url (str): URL to open in the WebDriver.
            time_out (int, optional): Timeout value for WebDriver wait (in seconds). Defaults to 10.
        """
        self.url: str = url
        self.driver_name: str = driver_name
        self.time_out: int = time_out
        self.driver: Optional[webdriver.Chrome] = None
        self.webdriver_wait: Optional[WebDriverWait] = None
        self.actions: Optional[ActionChains] = None

        self.selection_methods: dict = {
            "id": By.ID,
            "name": By.NAME,
            "class_name": By.CLASS_NAME,
            "tag_name": By.TAG_NAME,
            "link_text": By.LINK_TEXT,
            "partial_link_text": By.PARTIAL_LINK_TEXT,
            "xpath": By.XPATH,
            "css_selector": By.CSS_SELECTOR,
        }

    def __optionss(self) -> None:
        """
        Configure and return the ChromeOptions object for WebDriver options.

        Returns:
            ChromeOptions: Configured options for the WebDriver.
        """
        options = webdriver.ChromeOptions()

        # Set user-agent string
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
        )

        # Exclude "enable-automation" switch
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        # Disable Automation Extension
        options.add_experimental_option("useAutomationExtension", False)

        # Set preferences to disable browser notifications
        # prefs = {"profile.default_content_setting_values.notifications": 2}
        # options.add_experimental_option("prefs", prefs)

        # Disable automation controlled features of Chrome
        options.add_argument("--disable-blink-features=AutomationControlled")

        # Set a custom user-data directory for Chrome
        options.add_argument(
            r"--user-data-dir={0}".format(
                os.getcwd() + r"/{0}/".format(self.driver_name)
            )
        )

        return options

    def launch_driver(self) -> None:
        """
        Launches a Chrome WebDriver.
        """
        caps = DesiredCapabilities.CHROME
        caps["goog:loggingPrefs"] = {"performance": "ALL"}

        service = Service(ChromeDriverManager().install())

        driver = webdriver.Chrome(
            executable_path=os.getcwd() + r"/webdriver/chromedriver.exe",
            desired_capabilities=caps,
            options=self.__optionss(),
            service=service,
        )

        stealth(
            driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

        driver.get(self.url)

        self.driver = driver
        self.webdriver_wait = WebDriverWait(self.driver, self.time_out)
        self.actions = ActionChains(self.driver)

    def select(self, methode, path) -> WebElement:
        """
        Selects and returns a single element using the specified method and path.

        Dict:
            "id": By.ID,
            "name": By.NAME,
            "class_name": By.CLASS_NAME,
            "tag_name": By.TAG_NAME,
            "link_text": By.LINK_TEXT,
            "partial_link_text": By.PARTIAL_LINK_TEXT,
            "xpath": By.XPATH,
            "css_selector": By.CSS_SELECTOR

        Args:
            methode (str): Element selection method.
            path (str): Path or value for element selection.

        Returns:
            WebElement: Selected element.
        """
        element = self.webdriver_wait.until(
            EC.presence_of_element_located((self.selection_methods[methode], path))
        )

        return element

    def select_all(self, methode: str, path: str) -> list[WebElement]:
        """
        Selects and returns all elements matching the specified method and path.

        Dict:
            "id": By.ID,
            "name": By.NAME,
            "class_name": By.CLASS_NAME,
            "tag_name": By.TAG_NAME,
            "link_text": By.LINK_TEXT,
            "partial_link_text": By.PARTIAL_LINK_TEXT,
            "xpath": By.XPATH,
            "css_selector": By.CSS_SELECTOR

        Args:
            methode (str): Element selection method.
            path (str): Path or value for element selection.

        Returns:
            list: List of selected elements.
        """

        elements = self.webdriver_wait.until(
            EC.presence_of_all_elements_located((self.selection_methods[methode], path))
        )

        return elements

    def select_all_from_element(
        self, element: WebElement, methode: str, path: str
    ) -> list[WebElement]:
        """
        Selects and returns all elements matching the specified method and path.

        Dict:
            "id": By.ID,
            "name": By.NAME,
            "class_name": By.CLASS_NAME,
            "tag_name": By.TAG_NAME,
            "link_text": By.LINK_TEXT,
            "partial_link_text": By.PARTIAL_LINK_TEXT,
            "xpath": By.XPATH,
            "css_selector": By.CSS_SELECTOR

        Args:
            methode (str): Element selection method.
            path (str): Path or value for element selection.

        Returns:
            list: List of selected elements.
        """

        elements = element.find_elements(self.selection_methods[methode], path)

        return elements

    def find_elements_with_restrictions(
        self, tag_name, tag_restriction
    ) -> list[WebElement]:
        """
        Finds elements that contain a set of specified child elements.

        Args:
            tag_restriction (list): List of tag names representing restrictions.

        Returns:
            list: List of elements containing the specified child elements.
        """

        # Find all elements based on the provided restrictions

        elements = self.select_all("tag_name", tag_name)

        matching_elements = []
        for element in elements:
            children_present = [
                element.find_elements(By.TAG_NAME, tag) for tag in tag_restriction
            ]
            # Check if all specified child elements are present within the current element
            if all(children_present):
                matching_elements.append(element)

        return matching_elements

    def select_from_element(
        self, element: WebElement, methode: str, path: str
    ) -> WebElement:
        """
        Selects and returns a single element using the specified method and path.

        Dict:
            "id": By.ID,
            "name": By.NAME,
            "class_name": By.CLASS_NAME,
            "tag_name": By.TAG_NAME,
            "link_text": By.LINK_TEXT,
            "partial_link_text": By.PARTIAL_LINK_TEXT,
            "xpath": By.XPATH,
            "css_selector": By.CSS_SELECTOR

        Args:
            methode (str): Element selection method.
            path (str): Path or value for element selection.

        Returns:
            WebElement: Selected element.
        """
        element = element.find_element(self.selection_methods[methode], path)

        return element

    def get(self, url: str) -> None:
        """
        Navigates the WebDriver to the specified URL.

        Args:
            url (str): URL to navigate to.
        """
        self.driver.get(url)

    def click(self, element: WebElement) -> None:
        """
        Performs a click action on the specified element.

        Args:
            element (WebElement): The element to click.
        """
        self.actions.click(element).perform()

    def kill(self) -> None:
        """
        Kills the WebDriver and cleans up resources.
        """
        if self.driver is not None:
            self.driver.quit()
            self.driver = None
            self.webdriver_wait = None
            self.actions = None

    def put_text(self, element: WebElement, text: str) -> None:
        """
        Enters the specified text into the provided element.

        Args:
            element (WebElement): The element to enter text into.
            text (str): The text to enter into the element.
        """
        element.send_keys(text)

    def submit(self, element: WebElement) -> None:
        """
        Submits the form or triggers an action by hitting Enter on the specified element.

        Args:
            element (WebElement): The element to submit or trigger action on.
        """
        element.send_keys(Keys.ENTER)

    def print_page(self) -> None:
        """
        Simulates a Ctrl+P command to print the current page.
        """
        body = self.select("tag_name", "body")
        body.send_keys(Keys.CONTROL + "p")

    def scroll_all(self) -> None:
        """
        Scrolls to the bottom of the page using JavaScript.
        """
        script = "window.scrollTo(0, document.body.scrollHeight);"
        self.driver.execute_script(script)

    def get_source(self) -> str:
        """
        Retrieves the source code of the current page.

        Returns:
            str: Source code of the page.
        """
        source = self.driver.page_source
        return source

    def write_to_file(self, filename) -> None:
        """
        Writes the source code of the page to an HTML file.

        Args:
            filename (str): Name of the HTML file to write.

        Raises:
            IOError: If there is an error writing the file.
        """
        source = self.get_source()

        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(source)
            print(f"Source code written to file: {filename}")
        except IOError as e:
            print(f"Error writing file: {filename}")
            raise e

    def print_to_pdf(self, output_path) -> None:
        """
        Prints the content of the page to a PDF file.

        Args:
            output_path (str): Path to save the PDF file.
        """
        try:
            script = """
                var callback = function () {
                    var options = {
                        scale: 1,
                        format: 'A4',
                        printBackground: true,
                        displayHeaderFooter: false,
                        margin: {
                            top: '1cm',
                            right: '1cm',
                            bottom: '1cm',
                            left: '1cm'
                        }
                    };

                    return window.printToPDF(options, function(error, data) {
                        if (error) throw error;
                        return btoa(data);
                    });
                };
                callback();
            """

            encoded_pdf = self.driver.execute_cdp_cmd("Page.printToPDF", {})
            with open(output_path, "wb") as file:
                file.write(base64.b64decode(encoded_pdf["data"]))
            print(f"Page content printed to PDF: {output_path}")
        except WebDriverException as e:
            print(f"Error printing page content to PDF: {output_path}")
            raise e

    def scroll_to_bottom(self) -> None:
        """
        Scrolls to the bottom of the page.
        """
        for _ in range(3):
            body = self.select("tag_name", "body")
            body.send_keys(Keys.END)
            # Add a small delay between scrolls to allow content to load
            sleep(1)
            body.send_keys(Keys.HOME)
            sleep(1)
            body.send_keys(Keys.END)
