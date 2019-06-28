from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.keys import Keys

'''
    #system settings:
    #reload(sys)
    #sys.setdefaultencoding('utf-8')
    
    import sys
    # sys.setdefaultencoding() does not exist, here!
    reload(sys)  # Reload does the trick!
    sys.setdefaultencoding('UTF8')
    
    '''

category1 = 'jackets'
category2 = 'shirts'
category3 = 'sweatshirts'
category4 = 't-shirts'
category5 = 'hats'
category6 = 'accessories'
category7 = 'tops_sweaters'

color = 'Color'
size1 = 'Small'
size2 = 'Medium'
size3 = 'Large'
Name = 'Dream'


#buyer personal infor
buyerName = 'x X'
buyerMail = 'x@gmail.com'
buyerTele = 'xxx-xxx-xxx'
buyerAddress = 'xxx x x x'
buyerZIP = '606xx'

#buyer card info
buyerCardNumber = '1234 1234 1234 1234'
buyerCardExpMonth = '01'
buyerCardExpYear = '2020'

def shirt(category=category7, itemName='Terry', itemColor='Black', itemSize=size3, timeDelay = True):
    #Fixed variables
    arrayColor = []
    arrayColorCount = 0

    arrayColorLinks = []
    arrayColorLinkCount = 0

    indices = []
    indicesCount = 0

    new_list = []

    myItemLink = []
    myItemLinkCount = 0

    rightItemIndex = []

    URL_Prefix =  'http://www.supremenewyork.com/'
    URL_Midfix = 'shop/all/'


    #Driver Settings
    driver = webdriver.Firefox(executable_path='/Users/afzal/Downloads/geckodriver')

    #if variable timeDelay == True then (this gives time so user can login to google to avoid captchas)
    if timeDelay == True:
        time.sleep(3)

    #head to website
    supreme_url = str(URL_Prefix + URL_Midfix + category)
    driver.get(supreme_url)


    #BeautifulSoup settings
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    #find items
    for color in soup.find_all('a', attrs={"class": "name-link"}, href=True):
        arrayColor.append(color.text)
        arrayColorCount += 1

    print("Succesfully located items for latest drop!")
    print("In Total the List Contains : " + str(arrayColorCount) + " Elements")

    #find itemlinks
    for colorLink in soup.find_all('a', attrs={"class": "name-link"}, href=True):
        arrayColorLinks.append(colorLink.get('href'))
        arrayColorLinkCount += 1

    print("Succesfully found the links of items!")

    if arrayColorLinkCount == arrayColorCount:
        print ("Link count matches item count!")

    #find indexnumber of wanted item in arrays
    for i, elem in enumerate(arrayColor):
        if itemName in elem:
            indices.append(i)
            indicesCount += 1

    print("Keyword we are looking for was located : " + str(indicesCount) + " times!")
    print(indices)

    #find the correct links

    new_list = [x+1 for x in indices]

    #make a list out of the indexes that new_list contains
    for i, numb in enumerate(new_list):
        myItemLink.append(arrayColor[numb])
        myItemLinkCount += 1

    print("This item is available in " + str(myItemLinkCount) + " Colors: " + str(myItemLink))

    #pick right color
    for i, item in enumerate(myItemLink):
        if itemColor in item:
            rightItemIndex.append(i)

    print(rightItemIndex)

    #pick rightItemIndex in new_list so that I can later access link of item
    indexOfRightItem = new_list[rightItemIndex[0]]

    print(indexOfRightItem)

    #get Link
    supremeSuffixToCop = arrayColorLinks[indexOfRightItem]
    #print(supremeSuffixToCop)
    #go to link
    driver.get(str(URL_Prefix + supremeSuffixToCop))

    #wait until size dropdown is available
    wait = WebDriverWait(driver, 10)
    x = wait.until(EC.presence_of_element_located((By.ID, 's')))

    #select size
    Select(driver.find_element_by_id('s')).select_by_visible_text(itemSize)

    #add to cart
    driver.find_element_by_xpath('//*[@id="add-remove-buttons"]/input').click()

    #go to checkout
    driver.get("http://www.supremenewyork.com/checkout/")

    #fill out form
    while True:
        try:
            driver.find_element_by_id('order_billing_name')
            break
        except (NoSuchElementException):
            driver.get("http://www.supremenewyork.com/checkout")
            time.sleep(0.05)

    #Check Out Page Fill
    ord_billing_name=driver.find_element_by_id('order_billing_name')
    ord_billing_name.send_keys(buyerName)

    ord_email=driver.find_element_by_id('order_email')
    ord_email.send_keys(buyerMail)

    ord_tele=driver.find_element_by_id('order_tel')
    ord_tele.send_keys(buyerTele)

    ord_adress=driver.find_element_by_id('bo')
    ord_adress.send_keys(buyerAddress)

    ord_zip=driver.find_element_by_id('order_billing_zip')
    ord_zip.send_keys(buyerZIP)

    driver.find_element_by_xpath('//*[@id="cart-cc"]/fieldset/p[2]/label/div/ins').click()
    #clicks agree to terms box

    ord_cnb=driver.find_element_by_id('nnaerb')
    ord_cnb.send_keys(buyerCardNumber)

    Select(driver.find_element_by_id('credit_card_month')).select_by_visible_text(buyerCardExpMonth)
    Select(driver.find_element_by_id('credit_card_year')).select_by_visible_text(buyerCardExpYear)


