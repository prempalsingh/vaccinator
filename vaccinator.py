from datetime import date, timedelta
import requests
import sys
import os
import smtplib

PINCODE = 110027
AGE = 25

def get_next_10_dates():
	dates = []
	today = date.today()
	for _ in range(10):
		dates.append(today.strftime("%d-%m-%Y"))
		today = today + timedelta(days=1)
	return dates

def get_slots_for_date(d):
	print("Checking for date - " + d)
	url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode=" + str(PINCODE) + "&date=" + d
	response = requests.get(url, headers = {
		'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'
	})
	if response.status_code == 200:
		json_response = response.json()
		available_slots = [session for session in json_response["sessions"] if session["min_age_limit"] <= AGE and session["available_capacity"] > 0]
		if len(available_slots) > 0:
			return available_slots
		else:
			print("No slots found for date - " + d)
	else:
		print(response.text)
	return None

def send_email():
	sender_email = os.environ['SENDER_EMAIL']
	pwd = os.environ['SENDER_PWD']
	receiver_email = os.environ['RECEIVER_EMAIL']

	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.starttls()
	s.login(sender_email, pwd)
	message = 'Subject: {}\n\n{}'.format("Vaccinator: Vaccine slots available!", "")
	s.sendmail(sender_email, receiver_email, message)
	s.quit()


if __name__ == "__main__":
	dates = get_next_10_dates()
	available_slots = []
	for date in dates:
		slots = get_slots_for_date(date)
		if slots is not None:
			available_slots.extend(slots)
	if len(available_slots) > 0:
		print("Slots are available. Notifying...")
		send_email()
	
