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


class BaslerImgCollector:
    def __init__(self, output):
        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        self.output_stream = output
        self.is_grabbing = False

    def start(self):
        if self.is_grabbing:
            return

        self.is_grabbing = True
        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        self.camera.ExposureAuto.SetValue("Once")
        while self.camera.IsGrabbing() and self.is_grabbing:
            grabResult = self.camera.RetrieveResult(RES_TIMEOUT, pylon.TimeoutHandling_ThrowException)

            if grabResult.GrabSucceeded():
                image = converter.Convert(grabResult)
                img = image.GetArray()
                ret, buffer = cv2.imencode('.jpg', img)
                jpg = base64.b64encode(buffer).decode()
                self._publish(jpg)
                
            grabResult.Release()
        self.camera.StopGrabbing()

    def stop(self):
        self.is_grabbing = False

    def _publish(self, image):
        data = json.dumps({'data': image})
        bin = erlang.term_to_binary(data)
        header = pack('!I', len(bin))
        self.output_stream.write(header)
        self.output_stream.write(bin)
        self.output_stream.flush()

            


        
