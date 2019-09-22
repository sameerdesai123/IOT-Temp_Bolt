import email_config, json, time
from boltiot import Bolt, Email
minimum_limit = 300
maximum_limit = 600
mybolt = Bolt(email_config.API_KEY, email_config.DEVICE_ID)
mailer = Email(email_config.MAILGUN_API_KEY, email_config.SANDBOX_URL, email_config.SENDER_EMAIL, email_config.RECIPIENT_EMAIL)
while True:
    print ("Reading sensor value")
    response = mybolt.analogRead('A0')
    data = json.loads(response)
    print ("Sensor value is: " + str(data['value']))
    try:
        sensor_value = int(data['value'])
        if sensor_value > maximum_limit or sensor_value < minimum_limit:
            print("Making request to Mailgun to send an email")
            response = mailer.send_email("Alert", "The Current temperature sensor value is " +str(sensor_value))
            response_text = json.loads(response.text)
            print("Response received from Mailgun is: " + str(response_text['message']))
    except Exception as e:
        print ("Error occured: Below are the details")
        print (e)
    time.sleep(10)
