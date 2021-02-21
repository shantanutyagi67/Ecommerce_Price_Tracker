import urllib
from IPython.display import Image, display
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import smtplib
from selenium.webdriver.support.ui import WebDriverWait
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import time
import os
import math


def scrape(url, price, email):
    # browser options
    options = Options()
    options.add_argument('--headless')
    # create webdriver object
    driver = webdriver.Chrome(options=options)
    URL, myPrice, myEmail = url, price, email
    try:
        driver.get(URL)
    except:
        return "Invalid URL. Try again :("
    name = ""
    website = ""
    price = ""
    available = True

    # get element
    if URL[12:20] == "flipkart":
        # fixed class name for product name
        #WebDriverWait(driver,3)
        element = driver.find_element_by_class_name("B_NuCI").text
        name = element
        print(name)
        # fixed class name for product price
        element = driver.find_element_by_class_name("_16Jk6d").text
        price = element
        print(price)

        # used to distinguish 2 types of product images
        companyName = True
        try:
            # fixed class name if company name given
            element = driver.find_element_by_class_name("G6XhRU").text
            # print(element)
        except NoSuchElementException as exception:
            # class does not exist means no company name given
            companyName = False

        # product image
        if companyName:
            element = driver.find_element_by_class_name("_3kidJX").find_element_by_xpath(".//div[2]/div/img")
        else:
            element = driver.find_element_by_class_name("_3kidJX").find_element_by_xpath(".//div[2]/img")
        src = element.get_attribute('src')
        # print(src)
        urllib.request.urlretrieve(src, "")
        #display(Image(filename='prodImg.png'))
        # os.remove('pages/static/prodImg.png')
        website = "Flipkart"

    elif URL[12:18] == "amazon":
        # Check availability
        try:
            element = driver.find_element_by_id("availability").text
        except NoSuchElementException as exception:
            available = False
        if available:
            # distinguish b/w deal of day and normal product
            dayDeal = True
            try:
                # fixed class name if deal of day product
                element = driver.find_element_by_id("priceblock_dealprice_lbl").text
                # print(element)
            except NoSuchElementException as exception:
                # class does not exist means not deal of day product
                dayDeal = False

            # fixed class name for product name irrespective of deal of day or normal product
            element = driver.find_element_by_id("productTitle").text
            name = element
            print(name)
            if dayDeal:
                # if deal of day product then use corresponding id
                element = driver.find_element_by_id("priceblock_dealprice").text
                price = element
                print(price)
            else:
                # if normal product then use corresponding id
                element = driver.find_element_by_id("priceblock_ourprice").text
                price = element
                print(price)
            # product image
            element = driver.find_element_by_id("landingImage")
            src = element.get_attribute('src')
            # print(src)
            urllib.request.urlretrieve(src, "prodImg.png")
            #display(Image(filename="prodImg.png"))
            # os.remove('images\prodImg.png')
            website = "Amazon"
        else:
            return "Unavailable. Email will be sent when available within budget."

    elif URL[12:20] == "snapdeal":
        try:
            element = driver.find_element_by_class_name("sold-out-err").text
            available = False
        except NoSuchElementException as exception:
            available = True
        if available:
            # fixed class name for product name
            element = driver.find_element_by_class_name("pdp-e-i-head").text
            name = element
            print(name)
            # fixed class name for product price
            element = driver.find_element_by_class_name("payBlkBig").text
            price = "₹" + element
            print(price)

            # product image
            element = driver.find_element_by_class_name("cloudzoom")
            src = element.get_attribute('src')
            # print(src)
            urllib.request.urlretrieve(src, "prodImg.png")
            #display(Image(filename='prodImg.png'))
            # os.remove('images\prodImg.png')
            website = "Snapdeal"

        else:
            return "Unavailable. Email will be sent when available within budget."

    else:
        return "We dont work with this website :("

    # send email if conditions are satisfied
    price = price.replace(',', '')
    if available and name != "" and price != "" and int(myPrice) >= int(price[1:len(price)]) and website != "":
        mail_content = '''<pre>Hello Customer!<br>
    The product you looked for on %s is now available within your budget.<br>
    The datails are:
        Name: %s
        Price: %s
        <a href="%s">LINK</a>
        </pre>''' % (website, name, price, URL)
        # The mail addresses and password
        #validation = pd.read_csv(r'C:\Users\geekSA67\code\validation\validation.csv')
        sender_address = "shantanutyagi67@gmail.com"#validation['email'][0]
        sender_pass = "********"#validation['pass'][0]
        receiver_address = myEmail
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Product available within budget!'  # The subject line
        # The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'html'))

        # Attach the image of the product
        #filename = 'prodImg.png'
        #fp = open(filename, 'rb')
        #att = email.mime.application.MIMEApplication(fp.read(), _subtype="pdf")
        #fp.close()
        #att.add_header('Content-Disposition', 'attachment', filename=name)
        #message.attach(att)

        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(sender_address, sender_pass)  # login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        #os.remove('prodImg.png')
        print('Mail Sent')
        return True
    return False
