from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import argparse
from dotenv import load_dotenv
import os, time


def main(amount: float, email: str, password: str, from_number: str, to_number: str):
    print("Launching firefox headless browser...")
    options = Options()
    options.headless = True
    options.add_argument("--headless")
    service = Service(executable_path="/usr/bin/geckodriver")
    driver = webdriver.Firefox(options=options, service=service)
    driver.get("https://id.ee.co.uk/login")
    print("Navigating to https://id.ee.co.uk/login")
    print(f"Logging in with {email}...")
    try:
        try:
            element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "onetrust-reject-all-handler"))
            )
            element.click()
            print("Got popup, rejecting cookies...")
        except TimeoutException:
            print("No cookie popup.")
        time.sleep(2)
        print("Entering email...")
        email_input = driver.find_element(By.XPATH, '//*[@id="username"]')
        email_input.clear()
        email_input.send_keys(email)
        print("Submitting email...")
        button = driver.find_element(By.XPATH, '//*[@id="spoofSubmitButton"]')
        button.click()
        email_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="signInName"]'))
        )
        time.sleep(2)
        driver.execute_script("arguments[0].scrollIntoView();", email_input)
        email_input.clear()
        email_input.send_keys(email)
        print("Entering password...")
        button = driver.find_element(By.XPATH, '//*[@id="next"]')
        button.click()
        password_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="password"]'))
        )
        password_input.clear()
        password_input.send_keys(password)
        print("Submitting login details...")
        button = driver.find_element(By.XPATH, '//*[@id="next"]')
        button.click()
        WebDriverWait(driver, 30).until( # just to check all logged in
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div[1]/div/section/main/div[1]/div[2]/div[1]/div/div/div/span'))
        )
        print("Navigating to https://ee.co.uk/plans-subscriptions/mobile/data-gifting")
        driver.get("https://ee.co.uk/plans-subscriptions/mobile/data-gifting")
        print("Selecting gift settings...")
        from_dropdown_test = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#select2-supplierMsisdn-container > .select2-selection__placeholder"))
        )
        from_dropdown_test.click()
        from_list_item = driver.find_element(By.XPATH, f"//ul[@id='select2-supplierMsisdn-results']/li[@title='{from_number}']")
        from_list_item.click()
        to_dropdown = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#select2-consumerMsisdn-container > .select2-selection__placeholder"))
        )
        # driver.execute_script("arguments[0].scrollIntoView();", to_dropdown)
        to_dropdown.click()
        to_list_item = driver.find_element(By.XPATH, f"//ul[@id='select2-consumerMsisdn-results']/li[@title='{to_number}']")
        to_list_item.click()
        #other_amount_button = WebDriverWait(driver, 30).until(
            #EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[5]/div/div[2]/div[2]/div/section[3]/section/div/main/div[1]/div/div[4]/div[4]/div[9]/a')))
        other_amount_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.col-xs-4:nth-child(9) > a:nth-child(1)')))
        other_amount_button.click()
        other_amount_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, f'//*[@id="gifting-amount-number-{from_number}-copied"]')))
        other_amount_input.clear()
        other_amount_input.send_keys(str(amount))
        print("Gifting...")
        confirm_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'.js-modal-content > div:nth-child(1) > div:nth-child(5) > button:nth-child(1)')))
        time.sleep(2)
        confirm_button.click()
        time.sleep(2) # wait for other amount popup to go
        gift_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.data-gifting-page__gift-data-button > button:nth-child(1)'))
        )
        time.sleep(1)
        driver.execute_script("arguments[0].scrollIntoView();", gift_button)
        gift_button.click()
        # driver.execute_script('arguments[0].click()', gift_button)
        print("Confirming gift...")
        confirm_again_button = driver.find_element(By.CSS_SELECTOR, ".data-gifting-page__confirmation-buttons > form:nth-child(1) > button:nth-child(1)")
        time.sleep(0.1)
        confirm_again_button.click()
        print("Waiting for success confirmation... (this does NOT wait for a text to your phone, it simply checks for the green tick on the website)")
        try:
            success_notice = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="data-gifting-success_title"]'))
            )
            print(f"Successfully gifted {amount}GB from {from_number} to {to_number}.")
        except TimeoutException:
            print("Failed to gift :(")

    finally:
        driver.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="EEAutoGift", description="Automatically gift data from one profile to another on your EE account.", epilog="~ Developed by MrRazamataz (razbot.xyz)")
    parser.add_argument("--username", help="Your username.")
    parser.add_argument("--password", help="Your password.")
    parser.add_argument("--from-number", help="The number you're gifting data from.")
    parser.add_argument("--to-number", help="The number you're gifting data to.")
    parser.add_argument("--amount", help="The amount of data you're gifting. In GB.", type=float)
    args = parser.parse_args()

    if not os.path.exists(".env"):
        print("Please rename .env.example to .env and fill in the required fields.")
        exit()
    load_dotenv()
    try:
        amount = float(os.getenv("AMOUNT"))
    except ValueError:
        print("AMOUNT needs to be a float. Please update or use CLI args.")
        exit()
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    from_number = os.getenv("FROM_NUMBER")
    to_number = os.getenv("TO_NUMBER")

    # give priority to CLI args over .env
    if args.amount:
        amount = args.amount
    if args.username:
        email = args.username
    if args.password:
        password = args.password
    if args.from_number:
        from_number = args.from_number
    if args.to_number:
        to_number = args.to_number
    # check inputs
    if not amount or not email or not password or not from_number or not to_number:
        print("Please provide all required fields in .env or use CLI args.")
        exit()
    if len(email) == 0 or len(password) == 0 or len(from_number) == 0 or len(to_number) == 0:
        print("Please provide all required fields in .env or use CLI args.")
        exit()
    main(amount, email, password, from_number, to_number)
