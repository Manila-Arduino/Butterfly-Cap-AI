from typing import List, Sequence
from classes.Arduino import Arduino
from classes.BoxedObject import BoxedObject
from classes.OD_Custom import OD_Custom
from classes.OD_Default import OD_Default
from classes.Video import Video
from classes.Wrapper import Wrapper

# ? -------------------------------- CONSTANTS
cam_index = 0
img_width = 512
img_height = 512
input_layer_name = "input_layer_4"
output_layer_name = "output_0"

arduino_port = ""


# ? -------------------------------- CLASSES
arduino = Arduino(arduino_port)
video = Video(cam_index, img_width, img_height)

od_custom = OD_Custom(
    "detect.tflite",
    [
        "I. Leuconoe (Female)",
        "I. Leuconoe (Male)",
        "Papilio Lowi (Female)",
        "Papilio Lowi (Male)",
        "P. Demoleus (Female)",
        "P. Demoleus (Male)",
    ],
    0.2,
    img_width=img_width,
    img_height=img_height,
    max_object_size_percent=0.80,
)

# ? -------------------------------- VARIABLES


# ? -------------------------------- FUNCTIONS


def on_od_receive(max_object: BoxedObject, results: Sequence[BoxedObject]):
    print(
        f"Max object detected: {max_object.entity} with confidence {max_object.score:.2f}"
    )


def on_arduino_receive(s: str):
    # TODO 3 ------------------------------------------------
    pass


# ? -------------------------------- SETUP
def setup():
    pass


# ? -------------------------------- LOOP
def loop():
    #! VIDEO
    img = video.capture(display=False)

    #! OBJECT DETECTION
    img = od_custom.detect(img, on_od_receive)

    #! DISPLAY VIDEO
    video.displayImg(img)

    #! ARDUINO
    if arduino.available():
        arduino_str = arduino.read()
        print(f"Arduino received: {arduino_str}")
        on_arduino_receive(arduino_str)


# ? -------------------------------- ETC
setup()


def onExit():
    arduino.close()


Wrapper(
    loop,
    onExit=onExit,
    keyboardEvents=[
        ["d", video.save_image],  # type: ignore
    ],
)
