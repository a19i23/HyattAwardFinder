from selenium import webdriver
import credentials, time

# City where you want to go and date looking for
city = 'Austin'
checkInDate = 'Oct/06/2017'
checkOutDate = 'Oct/07/2017'
hotelLookingFor = 'Hyatt Place Austin Downtown'


options = webdriver.ChromeOptions()
#options.add_argument('headless')
# set window size
options.add_argument('window-size=1200x600')

# path to chrome driver
pathToChrome = '/Users/a19i23/PycharmProjects/PythonWebScraper/chromedriver'

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


for result in searchResults:
    hotelFound = result.find_element_by_class_name('property_name')
    if hotelFound.text == hotelLookingFor:
        selectHotelButton = result.find_element_by_class_name('check-rates-btn')
        selectHotelButton.click()
        hyattPointsCheckbox = driver.find_element_by_name('gp_points_rnr')
        hyattPointsCheckbox.click()

        # go through list and see what is contained
        listOfOptions = driver.find_elements_by_id('mycarousel')
        for option in listOfOptions:
            rateTab = option.find_element_by_class_name('rateTab')
            print(rateTab.text)
        break

# searching should be done now
driver.close()