
from ctypes import *
import random
import os
import cv2
import time
import darknet
import argparse
#from threading import Thread, enumerate
#from queue import Queue
import csv
from transmitter.log_handler import LogHandler
import config_file


def parser():
    parser = argparse.ArgumentParser(description="YOLO Object Detection")
    parser.add_argument("--weights", default="yolov4.weights",
                        help="yolo weights path")
    parser.add_argument("--dont_show", action='store_true',
                        help="windown inference display. For headless systems")
    parser.add_argument("--config_file", default="./cfg/yolov4.cfg",
                        help="path to config file")
    parser.add_argument("--data_file", default="./cfg/coco.data",
                        help="path to data file")
    parser.add_argument("--thresh", type=float, default=.25,
                        help="remove detections with confidence below this value")
    parser.add_argument("--output", default='data/',
                        help="output directory")
    return parser.parse_args()


def check_arguments_errors(args):
    assert 0 < args.thresh < 1, "Threshold should be a float between zero and one (non-inclusive)"
    if not os.path.exists(args.config_file):
        raise(ValueError("Invalid config path {}".format(
            os.path.abspath(args.config_file))))
    if not os.path.exists(args.weights):
        raise(ValueError("Invalid weight path {}".format(
            os.path.abspath(args.weights))))
    if not os.path.exists(args.data_file):
        raise(ValueError("Invalid data file path {}".format(
            os.path.abspath(args.data_file))))


def inference(darknet_image):
    prev_time = time.time()
    detections = darknet.detect_image(
        network, class_names, darknet_image, thresh=args.thresh)
    print("Inf time", time.time() - prev_time)
    return detections


def save_result(result, filename):
    tmp = f'{args.output}{os.path.basename(filename)[:-4]}.txt'
    with open(tmp, "w") as the_file:
        csv.register_dialect("custom", delimiter=" ", skipinitialspace=True)
        writer = csv.writer(the_file, dialect="custom")
        for tup in result:
            writer.writerow(tup)


def draw_result(result, filename, image_not_resized, image_resized, class_colors):
    image = darknet.draw_boxes(result, image_not_resized, class_colors)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    tmp = f'{args.output}{os.path.basename(filename)[:-4]}.jpg'
    cv2.imwrite(tmp, image)


def rescale_results(results, shape, width, height):
    newResults = []
    wScale = shape[1]/width
    hScale = shape[0]/height
    for class_name, score, box in results:
        newResults.append((class_name, score, (int(
            wScale*box[0]), int(hScale*box[1]), int(box[2]*wScale), int(box[3]*hScale))))
    return newResults


if __name__ == '__main__':

    args = parser()
    check_arguments_errors(args)
    network, class_names, class_colors = darknet.load_network(
        args.config_file,
        args.data_file,
        args.weights,
        batch_size=1
    )
    colorList = [(255, 122, 112),
                 (240, 228, 137),
                 (185, 252, 151),
                 (151, 180, 252)]
    class_colors = dict()
    for i, name in enumerate(class_names):
        class_colors[name] = colorList[i]
    width = darknet.network_width(network)
    height = darknet.network_height(network)
    darknet_image = darknet.make_image(width, height, 3)

    capture = cv2.VideoCapture(config_file.camera_address)

    if not(capture.isOpened()):
        print("Could not open video device")
    
    log = LogHandler()

    while True:

        ret, frame = capture.read()

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (width, height),
                                   interpolation=cv2.INTER_LINEAR)

        darknet.copy_image_from_bytes(darknet_image, frame_resized.tobytes())
        result = inference(darknet_image)
        result = rescale_results(result, frame.shape, width, height)
        print(frame.shape, width, height)
        # print(result)
        log.detection(result)
        # save_result(result, 'test.jpg')
        # draw_result(result, filename, frame, frame, class_colors)
