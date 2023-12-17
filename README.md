# BotX - Selenium Automation Class

`BotX` is a Python class designed to facilitate automated tasks and interactions with web elements using the Selenium WebDriver.

## Overview

This class provides a wide range of functionalities for web automation, including:

- Browser launch and configuration.
- Element selection and interaction.
- Navigation and page manipulation.
- Page source retrieval and actions like printing to PDF.

## Prerequisites

- Python 3.x
- Selenium WebDriver
- Chrome WebDriver (ChromeDriver)
- `webdriver_manager`
- `selenium_stealth`
- `base64` (Standard Python library)

## Installation

To use the `BotX` class:

1. Install Python 3.x from [Python's official website](https://www.python.org/downloads/).
2. Install necessary packages:
   ```
   pip install selenium webdriver_manager selenium_stealth
   ```
3. Download the Chrome WebDriver (ChromeDriver) and ensure its path is correctly set.

## Usage

1. Import the `BotX` class into your Python file:

   ```python
   from BotX import BotX
   ```

2. Instantiate the `BotX` class with the required parameters:

   ```python
   bot = BotX(driver_name="YourDriverName", url="https://example.com")
   ```

3. Utilize the various methods provided by the class for web automation tasks:

   ```python
   # Example: Launch the browser and navigate to a URL
   bot.launch_driver()

   # Example: Click on an element
   button_element = bot.select("id", "buttonId")
   bot.click(button_element)

   # Example: Find elements within a parent element that meet specific criteria
   parent_element = bot.select("tag_name", "parent_tag")
   tag_restriction = ["img", "a", "h2"]
   matching_elements = bot.find_elements_with_restrictions_within_parent(parent_element, tag_restriction)

   # Other methods can be used similarly for automation tasks
   ```

4. Remember to clean up resources after use:

   ```python
   bot.kill()
   ```
