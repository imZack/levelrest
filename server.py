from gevent.wsgi import WSGIServer
from levelrest.app import app
import os

# listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
# sockname = './' + os.path.basename(__file__) + '.sock'
# if os.path.exists(sockname):
#     os.remove(sockname)
# listener.bind(sockname)
# listener.listen(1)
port = os.environ.get("PORT", 5000)
http_server = WSGIServer(('', int(port)), app)
http_server.serve_forever()
