import os, sys
import cv2
import json
import erlang
import base64
from struct import unpack, pack

class ImageCollector:
    def __init__(self, output):
        self.output_stream = output
        self.should_collect = False
        self.cap = None

    def start(self):
        self.should_collect = True
        self.cap = cv2.VideoCapture(0)
        
        while self.should_collect:
            ret, image = self.cap.read()
            ret, buffer = cv2.imencode('.jpg', image)
            jpg = base64.b64encode(buffer).decode()
            self._publish(jpg)

    def stop(self):
        self.should_collect = False
        if self.cap:
            self.cap.release()

    def _publish(self, image):
        data = json.dumps({'data': image})
        bin = erlang.term_to_binary(data)
        header = pack('!I', len(bin))
        self.output_stream.write(header)
        self.output_stream.write(bin)
        self.output_stream.flush()
                

def parse_message(input):
    header = input.read(4)
    if len(header) != 4:
        return None

    (length,) = unpack('!I', header)
    payload = input.read(length).decode()

    if len(payload) != length:
        return None

    return json.loads(payload)


def run():
    input, output = os.fdopen(3, "rb"), os.fdopen(4, "wb")
    image_collector = ImageCollector(output)

    while True:
        msg = parse_message(input)
        if msg is None: break

        if msg['command'] == 'collect':
            image_collector.start()


if __name__ == '__main__':
    run()
    # input, output = os.fdopen(3, "rb"), os.fdopen(4, "wb")
    # image_collector = ImageCollector(output)
    
    # for message in message_parser(input):
    #     print(message)
    #     handle_message(message, image_collector)

    
