from pypylon import pylon
from struct import unpack, pack
import cv2
import base64
import json
import erlang


converter = pylon.ImageFormatConverter()

converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

RES_TIMEOUT = 5000

camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

class BaslerImgCollector:
    def __init__(self, output):

        self.output_stream = output
        self.is_grabbing = False

    def start(self):
        if self.is_grabbing:
            return

        self.is_grabbing = True
        camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        camera.ExposureAuto.SetValue("Once")
        while camera.IsGrabbing() and self.is_grabbing:
            grabResult = camera.RetrieveResult(RES_TIMEOUT, pylon.TimeoutHandling_ThrowException)

            if grabResult.GrabSucceeded():
                image = converter.Convert(grabResult)
                img = image.GetArray()
                ret, buffer = cv2.imencode('.jpg', img)
                jpg = base64.b64encode(buffer).decode()
                self._publish(jpg)
            grabResult.Release()

    def stop(self):
        camera.StopGrabbing()
        self.is_grabbing = False

    def _publish(self, image):
        data = json.dumps({'data': image})
        bin = erlang.term_to_binary(data)
        header = pack('!I', len(bin))
        self.output_stream.write(header)
        self.output_stream.write(bin)
        self.output_stream.flush()

            


        
