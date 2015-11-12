import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')

'''
class Guestbook(webapp2.RequestHandler):
    def post(self):
        self.response.write('<html><body>You wrote:<pre>')
        self.response.write(cgi.escape(self.request.get('content')))
        self.response.write('</pre></body></html>')
'''

class Producer(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(cgi.escape(self.request.get('content')))
#        self.response.write('Hello, World!')

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
## curl -X POST -H "Content-Type:application/json" -d '{"name":"health","tags" : [ "traffic", "sustainability" ]}' 127.0.0.1:5000/post
#
#    k = kinesis.connect_to_region('us-west-2')
if __name__ == '__main__':
    
    app.run(debug=True, port=5001)
    

'''
