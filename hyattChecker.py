from selenium import webdriver
import credentials, time, smtplib

# City where you want to go and date looking for
city = 'Austin'                 # edit this
checkInDate = 'Oct/06/2017'     # edit this
checkOutDate = 'Oct/07/2017'    # edit this
hotelLookingFor = 'Hyatt Place Austin Downtown' #edit this

messageHeader = checkInDate + " - "+ checkOutDate+ "\n" +"Award available at: " +hotelLookingFor + "\n\n"

awardsFound = False
def main():
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    # set window size
    options.add_argument('window-size=1024x768')

    # path to chrome driver
    pathToChrome = credentials.pathToChromeDriver

    # intialize the driver
    driver = webdriver.Chrome(executable_path=pathToChrome, chrome_options=options)

    driver.get('https://www.hyatt.com')
    driver.implicitly_wait(10)

    # find signin element and click
    signInElement = driver.find_element_by_class_name('dd-signin')
    signInElement.click()

    # find elements for user name and password
    signInMenu = driver.find_element_by_class_name('ui-sign-in')

    # elements within sign in menu
    username = signInMenu.find_element_by_name('username')
    password = signInMenu.find_element_by_name('password')
    signInButton = signInMenu.find_element_by_class_name('signin-button')

    # fill in credentials
    username.send_keys(credentials.user)
    password.send_keys(credentials.pw)

    # click sign in
    signInButton.click()

    # find city and check-in/out date elements
    locationInput = driver.find_element_by_name('location')
    checkInInput = driver.find_element_by_name('checkinDate')
    checkOutInput = driver.find_element_by_name('checkoutDate')
    findHotelsButton = driver.find_element_by_class_name('quickbookSearchFormButton')

    # have to clear the default input before entering new date.
    # clearing the first one clears both
    checkInInput.clear()

    # enter city and check-in/out dates provided above
    locationInput.send_keys(city)
    checkInInput.send_keys(checkInDate)
    checkOutInput.send_keys(checkOutDate)

    findHotelsButton.click()

    # results
    searchResults = driver.find_elements_by_class_name('search-result-item')

    awardMessage = ''
    for result in searchResults:
        hotelFound = result.find_element_by_class_name('property_name')
        if hotelFound.text == hotelLookingFor:
            selectHotelButton = result.find_element_by_class_name('check-rates-btn')
            selectHotelButton.click()
            hyattPointsCheckbox = driver.find_element_by_name('gp_points_rnr')
            hyattPointsCheckbox.click()
            time.sleep(3)
            # go through list and see what is contained
            listOfOptionsElement = driver.find_element_by_id('mycarousel')
            listOfRateType = listOfOptionsElement.find_elements_by_name('rate_type')
            i = 1
            for ratetype in listOfRateType:
                awardsFound = True
                awardMessage += str(i)+". "+ratetype.text + "\n\n"
                print(ratetype.text)
                i+=1
            break

    # searching should be done now
    driver.close()

    if awardsFound == True:
        emailBody = messageHeader + awardMessage
        subject = "Hyatt award notification"
        message = 'Subject: {}\n\n{}'.format(subject, emailBody)

        #send email
        sendemail(credentials.gmailUserName, #from
              credentials.gmailPassword, #to
              message,              #message
              credentials.gmailUserName,
              credentials.gmailSendAddress)


def sendemail(login, password, message, from_addr, to_addr):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(login, password)

    msg = message
    server.sendmail(from_addr, to_addr, msg)
    server.quit()


if __name__ == '__main__':
    main()