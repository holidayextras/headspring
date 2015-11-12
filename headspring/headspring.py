import webapp2
import cgi
import logging
import json
from apiclient import discovery
import base64
from oauth2client.client import GoogleCredentials

#import tools
#reload(tools)

#from tools import generate_id
NUM_RETRIES = 3

import datetime
import uuid

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
#    msg_payload = {'data': data_line}
#    msg_payload = data_line
    if msg_attributes:
        msg_payload['attributes'] = msg_attributes
    body = {'messages': [msg_payload]}
    resp = client.projects().topics().publish(
        topic=pubsub_topic, body=body).execute(num_retries=NUM_RETRIES)
    logging.info(resp)
#    logging.log(resp)
    return resp


def generate_id():
    """Generate an ID and timestamp"""

    return {'timestamp': datetime.datetime.utcnow().isoformat(),
            'id': uuid.uuid4().urn}


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')


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
#        self.response.write(cgi.escape(self.request.get('content')))
        self.response.write(self.request.get('content'))
##        self.response.write('Hello, World!')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/post', Producer),
], debug=True)

'''
import traceback
import uuid
import json
import hashlib

from flask import Flask, abort, jsonify, request

from tools import generate_id, get_pubsub_client as get_client

#stream_name_ = 'banana' 
#stream_name_ = 'appleCommander' 
STREAM_NAME = 'projects/hx-test/topics/badgerbear'
PUBSUB_SCOPES = ['https://www.googleapis.com/auth/pubsub']
NUM_RETRIES = 3
PROJ_NAME = "hx-test"

app = Flask(__name__)

##k.put_record("banana", json.dumps(dat), "partitionkey")
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
        k.put_record(stream_name_, json.dumps(reqdat_), hsh)
    except Exception as e:
        app.logger.error(e)
        app.logger.error('failed to put to stream ' + json.dumps(reqdat_))
        abort(503, 'Internal Error')
        return json.dumps({'response': 'failure'})
        
    return json.dumps({'response': 'success'})
#
##    return jsonify(**reqdat_)
#
## curl -X POST -H "Content-Type:application/json" -d '{"name":"health","tags" : [ "traffic", "sustainability" ]}' 127.0.0.1:8080/post
#
#    k = kinesis.connect_to_region('us-west-2')
if __name__ == '__main__':
    
    app.run(debug=True, port=5001)
    

'''

'''
    @classmethod
    def producer(cls, reqjson):
        """Generic JSON POST"""

        reqdat_ = generate_id()

        logging.debug('webservice processing request')
        logging.info(json.dumps(reqdat_))

        if not reqjson:
            logging.error('No json submitted')
            webapp2.abort(400, 'Cannot interpret JSON post')

        try:
            hsh = json.dumps(reqjson)
            print hsh
            resource_hash = hashlib.md5(hsh).hexdigest()
            print resource_hash
        except Exception as e:
            logging.debug('JSON is unhashable')
            webapp2.abort(400, 'Cannot interpret JSON post')

        reqdat_['resource'] = reqjson
        reqdat_['resource_hash'] = resource_hash

#    try:
#        logging.debug('writing to stream')
#        k.put_record(stream_name_, json.dumps(reqdat_), hsh)
#    except Exception as e:
#        logging.error(e)
#        logging.error('failed to put to stream ' + json.dumps(reqdat_))
#        webapp2.abort(503, 'Internal Error')
#        return {'response': 'failure'}
            
        return {'response': 'success'}
'''
