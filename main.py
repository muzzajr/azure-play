from flask import Flask, Response, request, jsonify
from MessageAnnouncer import MessageAnnouncer
import json

app = Flask(__name__)
announcer = MessageAnnouncer()


def format_sse(data: str, event=None) -> str:
    msg = f'data: {data}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    return msg


@app.route('/ping')
def ping():
    msg = format_sse(data='pong')
    announcer.announce(msg=msg)
    return {}, 200


@app.route('/api', methods=['GET','POST'])
def api():

    data = request.json
    return jsonify(data), 200


@app.route('/listen', methods=['GET'])
def listen():

    def stream():
        messages = announcer.listen()  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield msg

    return Response(stream(), mimetype='text/event-stream')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(host="0.0.0.0", threaded=True)
