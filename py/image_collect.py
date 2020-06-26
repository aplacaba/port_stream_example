import os, sys
import cv2
import json
import erlang
import base64
from struct import unpack, pack
import threading
from basler_img_collector import BaslerImgCollector

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

        self.cap.release()
        self.cap = None
        return

    def stop(self):
        self.should_collect = False

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
        print("Not allowed")
        return None

    (length,) = unpack('!I', header)
    payload = input.read(length).decode()
    print(payload)

    if len(payload) != length:
        return None

    return json.loads(payload)


def run():
    input, output = os.fdopen(3, "rb"), os.fdopen(4, "wb")
    image_collector = ImageCollector(output)
    basler = BaslerImgCollector(output)

    thread = threading.Thread(target=basler.start, args=())
    thread.daemon = True

    while True:
        msg = parse_message(input)
        if msg is None:
            basler.stop()
            break

        if msg['command'] == 'start':
            if not basler.is_grabbing:
                thread.start()
        elif msg['command'] == 'stop':
            basler.stop()
        else:
            print("Invalid command")

            
if __name__ == '__main__':
    run()
            
    
