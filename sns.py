import boto3
import config


class Subscribe(object):
    def __init__(self, telnumber):
        self.telnumber = telnumber
        self.boto_session = boto3.session.Session(
            region_name=config.SNS_TOPIC_REGION
        )

        self.messages = []

    def subscribe(self):
        sns = self.boto_session.resource('sns')
        topic = sns.Topic(config.SNS_TOPIC_ARN)
        topic.subscribe(
            Protocol='sms',
            Endpoint=self._phone_number_sanitizer()
        )

        self.messages.append(
            '{telnumber} has been subscribed to SMS updates.'.format(
                telnumber=self.telnumber
            )
        )

    def _phone_number_sanitizer(self):
        self.telnumber = self.telnumber.replace("-", "")

        if len(self.telnumber) <= 10:
            self.telnumber = '+1' + self.telnumber
        return self.telnumber
