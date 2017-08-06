import boto3
import config


class Updates(object):
    def __init__(self):
        self.boto_session = boto3.session.Session(region_name=config.SNS_TOPIC_REGION)
        self.s3_listing = self._bucket_listing()

    def current(self):
        try:
            s3 = self.boto_session.resource('s3')
            obj = s3.Object(config.S3_BUCKET, 'update.txt')
            return obj.get()['Body'].read().decode('utf-8')
        except Exception as e:
            print(e)
            return None

    def draws(self):
        draws_posted = []
        for race_file in self.s3_listing:
            file_name = race_file.get('Key', None)
            if file_name in self._potential_draw_updates():
                draws_posted.append({
                    'name': file_name,
                    'url': self._get_public_url(file_name)
                })
        return draws_posted

    def results(self):
        results_posted = []
        for race_file in self.s3_listing:
            file_name = race_file.get('Key', None)
            if file_name in self._potential_result_updates():
                results_posted.append({
                    'name': file_name,
                    'url': self._get_public_url(file_name)
                })
        return results_posted

    def _bucket_listing(self):
        client = self.boto_session.client('s3')
        response = client.list_objects(
            Bucket=config.S3_BUCKET
        )

        return response.get('Contents')

    def _get_public_url(self, filename):
        return "https://s3.amazonaws.com/{bucket}/{filename}".format(
            bucket=config.S3_BUCKET,
            filename=filename
        )

    def _potential_draw_updates(self):
        return [
            'open1_draw.html',
            'open2_draw.html',
            'youth_draw.html',
            'novice_draw.html',
            'senior_draw.html'
        ]

    def _potential_result_updates(self):
        return [
            'open1_results.html',
            'open2_results.html',
            'youth_results.html',
            'novice_results.html',
            'senior_results.html'
        ]