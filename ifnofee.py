import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions


url = "https://nyidanmark.dk/en-GB/You-want-to-apply/Study/Higher-education?anchor=howtoapply"

from_email = "741323402@qq.com"  
from_password = "nskpzervlmizbdei"  

to_email = "*******@**.**"  # <-----填写你的收件邮箱

chrome_options = ChromeOptions()

while True:

    driver = webdriver.Chrome(service=ChromeService(), options=chrome_options)
    driver.maximize_window()

    wait = WebDriverWait(driver, 10)

    try:
        driver.get(url)

        pay_the_fee_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Pay the fee")))
        pay_the_fee_button.click()

        input_box = wait.until(EC.visibility_of_element_located((By.NAME, "payfee")))

        input_box.send_keys("**-****-**") # <-----填写你的case order id

        payment_status_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Payment status']")))
        payment_status_button.click()

        payment_status = wait.until(EC.visibility_of_element_located((By.XPATH, "//p[contains(text(), 'Payment status:')]")))
        ifnofee = payment_status.find_element(By.XPATH, "./following-sibling::p").text

        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        print(current_time, "Payment Status:", ifnofee)

        if "Paid" not in ifnofee:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart

            subject = "Payment Status Update"
            body = f"{current_time} The payment status is now 'no fee'."
            message = MIMEMultipart()
            message["From"] = from_email
            message["To"] = to_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))

            with smtplib.SMTP("smtp.qq.com", 587) as server:
                server.starttls()
                server.login(from_email, from_password)
                server.sendmail(from_email, to_email, message.as_string())

            break

    except Exception as e:
        pass
    
    finally:
        driver.quit()

    time.sleep(3600)  # 设定每次查询的间隔时间，单位是秒，3600即为每小时查询一次