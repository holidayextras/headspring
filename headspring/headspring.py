import traceback
import uuid
import json
import hashlib
import base64
import logging

from oauth2client.client import GoogleCredentials
from apiclient import discovery
from flask import Flask, abort, jsonify, request

from tools import generate_id, get_pubsub_client as get_client

#stream_name_ = 'banana' 
#stream_name_ = 'appleCommander' 
STREAM_NAME = 'projects/hx-test/topics/badgerbear'
PUBSUB_SCOPES = ['https://www.googleapis.com/auth/pubsub']
NUM_RETRIES = 3
PROJ_NAME = "hx-test"

app = Flask(__name__)
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
#    logging.log(resp)
    return resp

#
#
#
@app.route('/')
def index():
    """Generic just because"""
    return 'producer!'

@app.route('/ping')
def ping():
    """health"""
    app.logger.info('health check')
    return 'pong'

@app.route('/post', methods=['POST'])
def producer():
    """Generic JSON POST"""

    reqdat_ = generate_id()
    client = get_pubsub_client()

    app.logger.debug('webservice processing request')
    app.logger.debug(json.dumps(reqdat_))

    if not request.json:
        app.logger.debug('No json submitted')
        abort(400, 'Cannot interpret JSON post')

    try:
        hsh = json.dumps(request.json)
        print hsh
        resource_hash = hashlib.md5(hsh).hexdigest()
        print resource_hash
    except Exception as e:
        app.logger.debug('JSON is unhashable')
        abort(400, 'Cannot interpret JSON post')

    reqdat_['resource'] = request.json
    reqdat_['resource_hash'] = resource_hash

    try:
        app.logger.debug('writing to stream')
        publish(client, 'projects/hx-test/topics/badgerbear', json.dumps(reqdat_))
#        k.put_record(stream_name_, json.dumps(reqdat_), hsh)
    except Exception as e:
        app.logger.error(e)
        app.logger.error('failed to put to stream ' + json.dumps(reqdat_))
        abort(503, 'Internal Error')
        return json.dumps({'response': 'failure'})
        
    return json.dumps({'response': 'success'})
#
##    return jsonify(**reqdat_)
#
## curl -X POST -H "Content-Type:application/json" -d '{"name":"health","tags" : [ "traffic", "sustainability" ]}' 127.0.0.1:5000/post
#
#    k = kinesis.connect_to_region('us-west-2')
if __name__ == '__main__':
    
    app.run(debug=True, port=5001)
    

