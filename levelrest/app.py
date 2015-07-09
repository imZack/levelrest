from flask import Flask
from flask import request
from flask import jsonify
import plyvel
import re

range_pattern = re.compile(ur"([\S]+)[\.]{3}([\S]+)")

prefix_symbol = "$"
app = Flask(__name__)
db = plyvel.DB("testdb", create_if_missing=True)


@app.route("/<path:path>", methods=["GET"])
def get(path):
    segments = path.split("/")
    range_index = "".join(segments[-1:])
    prefix = str(prefix_symbol.join(segments[:-1]) + prefix_symbol)

    if len(segments) == 1:
        range_index = path
        prefix = ''

    match = re.search(range_pattern, range_index)
    if match is not None:
        # range get
        reverse = False
        start_key = prefix + str(match.group(1))
        stop_key = prefix + str(match.group(2))
        result = []
        for key, value in db.iterator(
            start=start_key, stop=stop_key,
            include_stop=True,
            reverse=reverse
        ):
            result.append({"key": key, "value": value})
            print "key %s, value %s" % (key, value)
        return jsonify(data=result)

    key = str((prefix_symbol.join(path.split("/"))))
    value = db.get(key)
    if value is not None:
        return jsonify({
            "key": key,
            "value": value
        })

    return jsonify(message="Not Found"), 404


@app.route("/<path:path>", methods=["POST", "PUT"])
def put(path):
    key = str((prefix_symbol.join(path.split("/"))))
    db.put(str(key), request.data)
    return "%s %s" % (path, request.data)


@app.route("/batch", methods=["POST", "PUT"])
def batch_put():
    data = request.get_json(silent=True)
    if data is None or data is False:
        return jsonify(message="Invaild format"), 400

    if isinstance(data, dict):
        data = [data]
    with db.write_batch() as wb:
        for obj in data:
            wb.put(str(obj["key"]), str(obj["value"]))

    return jsonify(message="OK")


@app.route("/<path:path>", methods=["DELETE"])
def delete_route(path):
    path = (prefix_symbol.join(path.split("/")))
    db.delete(str(path))
    return jsonify(message="OK")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
    db.close()
