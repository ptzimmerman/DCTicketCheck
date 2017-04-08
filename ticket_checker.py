from splinter import Browser
import cv2
import time
from pytesseract import image_to_string
from PIL import Image
from twilio.rest import Client

###########################

YOUR_LICENSE_PLATE = '' # DC-1234
YOUR_STATE = '' # Texas
YOUR_TWILIO_SID = ''
YOUR_TWILIO_AUTH_TOKEN = ''
YOUR_CELL = '' # 1234567890
YOUR_TWILIO_NUMBER = '' # 1234567890

###########################


browser = Browser()
browser.visit('https://prodpci.etimspayments.com/pbw/include/dc_parking/input.jsp?ticketType=P')

continue_attempts = True
while(continue_attempts):
	browser.driver.save_screenshot('screenshot.png')
	img = browser.driver.find_element_by_xpath('//*[@id="captcha"]')
	loc = img.location

	image = cv2.imread('screenshot.png',True)
	y_offset = 1050
	x_offset = 460
	roi = image[y_offset:y_offset+85, x_offset:x_offset+210]
	cv2.imwrite("cropped.jpeg", roi)

	captcha_text = image_to_string(Image.open('cropped.jpeg'))

	license_plate = YOUR_LICENSE_PLATE
	plate_field = browser.find_by_name('plateNumber')
	plate_field.fill(license_plate)

	dropdown = browser.find_by_xpath("/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td/div/table/tbody/tr/td[2]/table[1]/tbody/tr[2]/td/table/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[4]/td[1]/select")
	for option in dropdown.find_by_tag('option'):
		if option.text == YOUR_STATE: #EXAMPLE: "Texas"
        		option.click()
        		break

	captcha_field = browser.find_by_name('captchaSText')
	captcha_field.fill(captcha_text.replace(' ', ''))
	submit_button = browser.driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td/div/table/tbody/tr/td[2]/table[1]/tbody/tr[2]/td/table/tbody/tr/td/form/table/tbody/tr[3]/td/input[1]')
	submit_button.click()

	time.sleep(3)

	output = browser.driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td/div/table/tbody/tr/td[2]/table[1]/tbody/tr[2]/td/table/tbody/tr/td/form/table/tbody/tr[1]/td/li')

	error_string = 'Please enter the characters as shown in the box below to move to the next page.'
	if output.text == error_string:
		continue
	else:
		continue_attempts = False

# send sms
account_sid = YOUR_TWILIO_SID
auth_token = YOUR_TWILIO_AUTH_TOKEN

text_body = "For plate [%s]: " % license_plate
text_body += output.text

client = Client(account_sid, auth_token)
message = client.api.account.messages.create(to=YOUR_CELL,
                                             from_=YOUR_TWILIO_NUMBER,
                                             body=text_body)

browser.quit()
