import os
from gevent.wsgi import WSGIServer
from gevent import socket
from levelrest.app import app

# listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
# sockname = './' + os.path.basename(__file__) + '.sock'
# if os.path.exists(sockname):
#     os.remove(sockname)
# listener.bind(sockname)
# listener.listen(1)

http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()
