import twilio
import unittest
from twilio.rest import TwilioRestClient
from core_app.correo.sms_sender import SenderSMS

#Class that group the JUnit test for SenderSMS
class SenderSMS_Test(unittest.TestCase):
	DEFAULT_SENT_TO_NUMBER = "+573154150444"
	DEFAULT_SENT_FROM_NUMBER = "+15005550006"
	DEFAULT_TESTING_MODE = True
		
	#+15005550001	This phone number is invalid.	21212
	def test_from_number_invalid(self):
		try:
			my_sms_client = SenderSMS("+15005550001", self.DEFAULT_TESTING_MODE)
			response = my_sms_client.send_sms("::: test_from_number_invalid", self.DEFAULT_SENT_TO_NUMBER)
		except twilio.TwilioRestException as e:
			self.assertRaises(twilio.TwilioRestException)
			self.assertEqual(21212, e.code)
		
		
	#+15005550007	This phone number is not owned by your account or is not SMS-capable.	21606
	def test_from_number_not_owned_in_my_account(self):
		try:
			my_sms_client = SenderSMS("+15005550007", self.DEFAULT_TESTING_MODE)
			response = my_sms_client.send_sms("::: test_from_number_not_owned_in_my_account", self.DEFAULT_SENT_TO_NUMBER)
		except twilio.TwilioRestException as e:
			self.assertRaises(twilio.TwilioRestException)
			self.assertEqual(21606, e.code)
	
	#+15005550008	This number has an SMS message queue that is full.	21611
	def test_from_number_sms_queue_full(self):
		try:
			my_sms_client = SenderSMS("+15005550008", self.DEFAULT_TESTING_MODE)
			response = my_sms_client.send_sms("::: test_from_number_sms_queue_full", self.DEFAULT_SENT_TO_NUMBER)
		except twilio.TwilioRestException as e:
			self.assertRaises(twilio.TwilioRestException)
			self.assertEqual(21611, e.code)
		
	#+15005550006	This number passes all validation.	No error
	def test_from_number_OK(self):
		my_sms_client = SenderSMS(self.DEFAULT_SENT_FROM_NUMBER, self.DEFAULT_TESTING_MODE)
		response = my_sms_client.send_sms("::: test_from_number_OK", self.DEFAULT_SENT_TO_NUMBER)
		self.assertIsNotNone(response)
		self.assertIsNotNone(response.sid)
	
	#+15005550001	This phone number is invalid.	21211
	def test_to_number_invalid(self):
		try:
			my_sms_client = SenderSMS(self.DEFAULT_SENT_FROM_NUMBER, self.DEFAULT_TESTING_MODE)
			response = my_sms_client.send_sms("::: test_to_number_invalid", "+15005550001")
		except twilio.TwilioRestException as e:
			self.assertRaises(twilio.TwilioRestException)
			self.assertEqual(21211, e.code)
		
	#+15005550002	Twilio cannot route to this number.	21612
	def test_to_number_cant_be_routed(self):
		try:
			my_sms_client = SenderSMS(self.DEFAULT_SENT_FROM_NUMBER, self.DEFAULT_TESTING_MODE)
			response = my_sms_client.send_sms("::: test_to_number_cant_be_routed", "+15005550002")
		except twilio.TwilioRestException as e:
			self.assertRaises(twilio.TwilioRestException)
			self.assertEqual(21612, e.code)
		
	#+15005550003	Your account doesn't have the international permissions necessary to SMS this number.	21408
	def test_to_number_invalid_permissions(self):
		try:
			my_sms_client = SenderSMS(self.DEFAULT_SENT_FROM_NUMBER, self.DEFAULT_TESTING_MODE)
			response = my_sms_client.send_sms("::: test_to_number_invalid_permissions", "+15005550003")
		except twilio.TwilioRestException as e:
			self.assertRaises(twilio.TwilioRestException)
			self.assertEqual(21408, e.code)
		
	#+15005550004	This number is blacklisted for your account.	21610	
	def test_to_number_in_blacklist(self):
		try:
			my_sms_client = SenderSMS(self.DEFAULT_SENT_FROM_NUMBER, self.DEFAULT_TESTING_MODE)
			response = my_sms_client.send_sms("::: test_to_number_in_blacklist", "+15005550004")
		except twilio.TwilioRestException as e:
			self.assertRaises(twilio.TwilioRestException)
			self.assertEqual(21610, e.code)
		
	#+15005550009	This number is incapable of receiving SMS messages.	21614	
	def test_to_number_incapable_to_receiving_sms(self):
		try:
			my_sms_client = SenderSMS(self.DEFAULT_SENT_FROM_NUMBER, self.DEFAULT_TESTING_MODE)
			response = my_sms_client.send_sms("::: test_to_number_in_blacklist", "+15005550009")
		except twilio.TwilioRestException as e:
			self.assertRaises(twilio.TwilioRestException)
			self.assertEqual(21614, e.code)
		
if __name__ == '__main__':
    unittest.main()