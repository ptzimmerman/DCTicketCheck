# DCTicketCheck
Checking for tickets in DC via their system sucks. Here's my better way even after a gallon of beer. This wouldn't be required if their automatic notification system wasn't crap/completely non-functional. Getting notified on a daily basis of your balance is nice since photo tickets never seem to make it via snail mail...and good luck fighting late fees that accrue.

DC has a system where you can check if you have any tickets: https://prodpci.etimspayments.com/pbw/include/dc_parking/input.jsp?ticketType=P

This site has at least some bot checks so requests won't work (despite altering the UA). 

There's probably a better way than having to compile OpenCV. Regardless, you'll need the absolutle newest version of geckodriver (old versions tend to break selenium on a weekly basis).
https://github.com/mozilla/geckodriver/releases
