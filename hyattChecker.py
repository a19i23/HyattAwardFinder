from selenium import webdriver
import credentials

options = webdriver.ChromeOptions()
#options.add_argument('headless')
# set window size
options.add_argument('window-size=1200x600')

# path to chrome driver
pathToChrome = '/Users/a19i23/PycharmProjects/PythonWebScraper/chromedriver'

# intialize the driver
driver = webdriver.Chrome(executable_path=pathToChrome, chrome_options=options)

driver.get('https://www.hyatt.com')

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