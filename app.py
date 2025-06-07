is_rpi = True  # TODO: Change this to True if running on Raspberry Pi

from typing import List, Sequence
from classes.Arduino import Arduino
from classes.BoxedObject import BoxedObject
from classes.OD_Custom import OD_Custom
from classes.OD_Default import OD_Default
from classes.Video import Video
from classes.Wrapper import Wrapper
from decorators.execute_interval import execute_interval

# ? -------------------------------- CONSTANTS
cam_index = 0
img_width = 512
img_height = 512
input_layer_name = "input_layer_4"
output_layer_name = "output_0"

arduino_port = "/dev/ttyUSB0"
if is_rpi:
    from classes.ShutdownButton import ShutdownButton

    shutdown_button = ShutdownButton(16)

entities = [
    "I. Leuconoe (Female)",
    "I. Leuconoe (Male)",
    "Papilio Lowi (Female)",
    "Papilio Lowi (Male)",
    "P. Demoleus (Female)",
    "P. Demoleus (Male)",
]

# ? -------------------------------- CLASSES
arduino = Arduino(arduino_port)
video = Video(cam_index, img_width, img_height)

od_custom = OD_Custom(
    "/home/pi/Desktop/ai/detect.tflite",
    entities,
    0.05,
    img_width=img_width,
    img_height=img_height,
    max_object_size_percent=0.80,
)

# ? -------------------------------- VARIABLES
nameInt = 0
genderInt = 0


# ? -------------------------------- FUNCTIONS
def index_or_minus1(my_list, value):
    try:
        return my_list.index(value)
    except ValueError:
        return -1


@execute_interval(1)
def arduino_send():
    global nameInt, genderInt

    arduino_str = f"{nameInt},{genderInt}"
    print(f"Sending to Arduino: {arduino_str}")
    arduino.println(arduino_str)


def on_od_receive(max_object: BoxedObject, results: Sequence[BoxedObject]):
    global nameInt, genderInt

    print(
        f"Max object detected: {max_object.entity} with confidence {max_object.score:.2f}"
    )

    index = index_or_minus1(entities, max_object.entity)

    if index == 0:
        nameInt = 1
        genderInt = 2

    elif index == 1:
        nameInt = 1
        genderInt = 1

    elif index == 2:
        nameInt = 2
        genderInt = 2

    elif index == 3:
        nameInt = 2
        genderInt = 1

    elif index == 4:
        nameInt = 3
        genderInt = 2

    elif index == 5:
        nameInt = 3
        genderInt = 1

    else:
        nameInt = 0
        genderInt = 0

    if nameInt != 0 and genderInt != 0:
        arduino_send()


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
