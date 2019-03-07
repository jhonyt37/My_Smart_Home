from twilio.rest import TwilioRestClient

#This class needs to run this command to work: $ pip install twilio
class SenderSMS():
	FROM_PHONE_NUMBER_PROD = "+15208674780"
	# ======================== 	Production credentials	=========================
	account_sid_prod = "AC66c4bbcc65f97595ea05b798e366e92c"
	auth_token_prod  = "f4012b86d339064dbf356978e3ee8967"
	# ======================== 	Test Credentials	=============================
	account_sid_test = "AC4a02c06787cb6792850828af61ce7205"
	auth_token_test  = "1ade2a7aa7ff7be3708082851dcc7f04"
	
	#Method that initialize the values for required behavior
	def __init__(self, from_number="0", testing_mode = True):
		self.testing_mode = True
		self.testing_mode = testing_mode		
		
		if testing_mode:
			self.from_phone_number = from_number
			self.client = TwilioRestClient(self.account_sid_test, self.auth_token_test)
		else:
			self.from_phone_number = self.FROM_PHONE_NUMBER_PROD
			self.client = TwilioRestClient(self.account_sid_prod, self.auth_token_prod)
	
	#Method that sends a sms text message to a given number
	def send_sms(self, text_message, send_to_number):
		message = self.client.messages.create(body=text_message,to=send_to_number, from_=self.from_phone_number)
		print("Message send - MessageId = ", message.sid)
		return message

#Run this code to check if sms is sent properly
#my_sms_client = SMS_Sender()
#my_sms_client.send_sms("Mensaje de prueba X", "+573154150444")