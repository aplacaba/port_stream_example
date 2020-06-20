import os, sys
import cv2
import json
import erlang
import base64
from struct import unpack

should_collect = False
cap = None

def send_to_genserver(payload, output):
    data = json.dumps({'data': payload})
    bin = erlang.term_to_binary(data)
    header = pack('!I', bin)
    stream.write(header)
    stream.write(bin)
    stream.flush()

    
def collect_images(message, output):
    while should_collect:
        cap = cv2.VideoCapture(0)
        ret, image = cap.read()
        ret, buffer = cv2.imencode('.jpg', image)
        jpg = base64.b64encode(buffer)
        send_to_genserver(buffer, output)
        
        
def handle_message(message, output):
    if message['command'] == 'collect':
        should_collect = True
        collect_images(output)
    else:
        should_collect = False
        if cap:
            cap.release()

    return None


def mesage_parser(input):
    header = stream.read(4)
    if len(header) != 4:
        return None

    (length,) = unpack('!I', header)
    payload = stream.read(length).decode()

    if len(payload) != length:
        return None

    return payload

if __name__ == '__main__':
    input, output = os.fdopen(3, "rb"), os.fdopen(4, "wb")
    
    for message in message_parser(input):
        handle_message(message, output)

    
