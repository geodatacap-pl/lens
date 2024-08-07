import time
from log_handler import LogHandler

testResult = [
        ("faceFront", 90, (400,400,250,250)),
        ("faceFront", 80, (400,400,250,250)),
        ("faceSide", 90, (400,400,250,250)),
        ("faceSide", 20, (400,400,250,250)),
        ("person", 90, (400,400,250,250)),
        ]

dataTest = LogHandler()

while True:
    dataTest.detection(testResult)
    time.sleep(1)
