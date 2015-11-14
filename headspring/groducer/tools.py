import datetime
import uuid
import httplib2
from apiclient import discovery

from oauth2client.client import GoogleCredentials

def generate_id():
    """Generate an ID and timestamp"""

    return {'timestamp': datetime.datetime.utcnow().isoformat(),
            'id': uuid.uuid4().urn}


def get_pubsub_client(version='v1beta2'):
    """Build the pubsub client."""

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
    return resp


if __name__ == '__main__':
    print generate_id()
    client = get_pubsub_client()
    print client
