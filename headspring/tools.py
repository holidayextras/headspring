"""
Tools for running the headspring app.

includes:

get_config_parser: for parsing config file for app

app_dir_switch: for moving into app directory

generate_id: for generating a timestamp and urn

get_pubsub_client: for getting the Google pubsub client

publish: publishing to pubsub
"""

import base64
import datetime
import httplib2
import os
import sys
import uuid
from apiclient import discovery

from ConfigParser import ConfigParser
from oauth2client.client import GoogleCredentials


def get_config_parser(filename, logging):
    """Open logging file"""

    config = ConfigParser()

    try:
        with open(filename) as _fp:
            config.readfp(_fp)
    except Exception:
        logging.info('failed to open config file')
        raise Exception('failed to open config file')

    return config


def app_dir_switch():
    """Switch into working directory"""

    os.chdir(os.path.dirname(sys.argv[0]))  # change into execution directory


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


def publish(client, pubsub_topic, data_line, logging, num_retries=3, msg_attributes=None):
    """Publish to the given pubsub topic."""
    data = base64.b64encode(data_line)
    msg_payload = {'data': data}
    if msg_attributes:
        msg_payload['attributes'] = msg_attributes
    body = {'messages': [msg_payload]}
    resp = client.projects().topics().publish(
        topic=pubsub_topic, body=body).execute(num_retries=num_retries)
    logging.info(resp)
    return resp
#
#if __name__ == '__main__':
#    print generate_id()
#    client = get_pubsub_client()
#    print client
