import base64
import datetime
import json
import logging
import uuid
import webapp2
from apiclient import discovery
from oauth2client.client import GoogleCredentials

NUM_RETRIES = 3


def get_pubsub_client(version='v1beta2'):
    """Build the pubsub client."""

    import httplib2
    get_pubsub_client.PUBSUB_SCOPES = ['https://www.googleapis.com/auth/pubsub']
    credentials = GoogleCredentials.get_application_default()

    if credentials.create_scoped_required():
        credentials = credentials.create_scoped(get_pubsub_client.PUBSUB_SCOPES)

    http = httplib2.Http()
    credentials.authorize(http)

    return discovery.build('pubsub', version, http=http)


def publish(client, pubsub_topic, data_line, msg_attributes=None):
    """Publish to the given pubsub topic."""
    data = base64.b64encode(data_line)
    msg_payload = {'data': data}
    if msg_attributes:
        msg_payload['attributes'] = msg_attributes
    body = {'messages': [msg_payload]}
    resp = client.projects().topics().publish(
        topic=pubsub_topic, body=body).execute(num_retries=NUM_RETRIES)
    logging.info(resp)
    return resp


def generate_id():
    """Generate an ID and timestamp"""

    return {'timestamp': datetime.datetime.utcnow().isoformat(),
            'id': uuid.uuid4().urn}


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Bears!')


class Producer(webapp2.RequestHandler):

    def post(self):
        client = get_pubsub_client()
        self.response.headers['Content-Type'] = 'application/json'

        dat = self.request.body
        try:
            dat = json.loads(dat)
        except Exception as e:
            raise TypeError
        logging.info('loading name {}'.format(dat.get('name')))
        logging.info(json.dumps(dat))
        publish(client, 'projects/hx-test/topics/badgerbear', json.dumps(dat))
        self.response.write(json.dumps(dat))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/post', Producer),
], debug=True)
