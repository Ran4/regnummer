from enum import Enum
import re
import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def get_regnummer():
    args = sys.argv[1:]
    if len(args) != 1:
        print("Usage: regnummer MSZ541")
        exit(1)

    else:
        return args[0]


class NoCarTaxFound(Exception):
    pass


def get_car_tax(driver, regnummer: str) -> int:
    """
    Raises:
        NoCarTaxFound
    """
    driver.get("https://bilskatt.nu")
    regnummer_input = driver.find_element_by_id("regnrinput")
    regnummer_input.send_keys(regnummer)
    regnummer_input.send_keys(Keys.ENTER)

    h3s = driver.find_elements_by_xpath("//h3")

    for h3 in h3s:
        match = re.match("årlig skatt: (?P<skatt>.+) sek", h3.text.lower())
        if match:
            skatt_str = match.group("skatt")
            return int(skatt_str)

    raise NoCarTaxFound()


class CarInsuranceType(Enum):
    HALVFORSAKRING = "HALVFORSAKRING"


def get_car_insurance_costs(driver, regnummer: str) -> int:
    return "NOT IMPLEMENTED"


def main():
    regnummer: str = get_regnummer()

    driver = webdriver.Chrome('./chromedriver')

    # When asking to get elements, if they don't exist, try for up to 5 seconds
    driver.implicitly_wait(5)

    try:
        car_tax = get_car_tax(driver, regnummer)
    except NoCarTaxFound:
        car_tax = None
    print(f"Car tax: {car_tax} kr/mån")

    car_insurance_costs = get_car_insurance_costs(driver, regnummer)
    print(f"Car insurance costs: {car_insurance_costs}")


if __name__ == "__main__":
    main()
