import boto3
from botocore.exceptions import ClientError

def send_email(body_text, body_html):
    sender = "Kim Stonehouse <kimbethstonehouse@gmail.com>"
    recipient = "Kim Stonehouse <kimbethstonehouse@gmail.com>"
    bcc1 = "Sola Onifade <solamipeonifade@gmail.com>"
    bcc2 = "Tiffany Choi <jwow5231@naver.com>"

    subject = "From Alexa: Your upcoming trip information"

    client = boto3.client('ses')

    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    recipient,
                ],
                'BccAddresses': [
                    bcc1,
                    bcc2,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': 'UTF-8',
                        'Data': body_html,
                    },
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': subject,
                },
            },
            Source=sender,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

    return
