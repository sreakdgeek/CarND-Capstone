from styx_msgs.msg import TrafficLight
import os
import sys
from PIL import Image
import numpy as np
import tensorflow as tf
import time
import sys

class TLClassifier(object):

    # Helper method to load inference graph
    def load_graph(self, graph_file):
        graph = tf.Graph()
        with graph.as_default():
           od_graph_def = tf.GraphDef()
           with tf.gfile.GFile(graph_file, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
        return graph

    # Converts image into to numpy array
    def load_image_into_numpy_array(self, image):
        (im_width, im_height) = (image.shape[1], image.shape[0])
        return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)

    def __init__(self, is_site):
        # Different models for simulator vs udacity parking lot
        sys.path.insert(0, '/home/neo/Downloads/ObjectDetectionAPI/models/research/object_detection')
        self.threshold = 0.5
        self.light_counter = 0
        if (is_site == False):
            print("Current path = " + os.getcwd())
            print("Simulator is true hence running simulator inference graph")
            frozen_graph_path = os.getcwd() + '/light_classification/models/sim/frozen_inference_graph.pb'
        else:
            print("Realworld is true hence running real world inference graph")
            frozen_graph_path = os.getcwd() + '/light_classification/models/real_world/frozen_inference_graph.pb'

        label_path = os.getcwd() + '/light_classification/models/label.pbtxt'
        self.detection_graph = self.load_graph(frozen_graph_path)
        self.num_classes = 3
        with self.detection_graph.as_default():
             self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
             self.detect_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
             self.detect_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
             self.detect_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
             self.num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

        self.sess = tf.Session(graph=self.detection_graph)
        pass

    def get_classification(self, image):
        """Determines the color of the traffic light in the image

        Args:
            image (cv::Mat): image containing the traffic light

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        #implement light color prediction
        #self.light_counter += 1
        #if  (self.light_counter  % 2 != 0):
        #    return TrafficLight.UNKNOWN

        print("image type = " + str(type(image)))
        print("image shape = " + str((image.shape)))
        #image_np = self.load_image_into_numpy_array(image)
        (im_width, im_height) = (image.shape[1], image.shape[0])
        image_np = np.array(image).reshape((im_height, im_width, 3)).astype(np.uint8)
        image_expanded = np.expand_dims(image_np, axis=0)

        # Inference
        time0 = time.time()
        (boxes, scores, classes, num) = self.sess.run(
                       [self.detect_boxes, self.detect_scores, self.detect_classes, self.num_detections],
                       feed_dict={self.image_tensor: image_expanded})
        time1 = time.time()
        print("Time in milliseconds", (time1 - time0) * 1000)
        print("scores[0] = " + str(scores[0]))
        print("classes[0] = " + str(classes[0]))

        boxes = np.squeeze(boxes)
        scores = np.squeeze(scores)
        classes = np.squeeze(classes).astype(np.int32)

        if (scores[0] > self.threshold):
              if (classes[0] == 1):
                 print("It is green signal now. Can start now")
                 return TrafficLight.GREEN
              elif (classes[0] == 2):
                 print("It is red signal. Need to stop.")
                 return TrafficLight.RED
              elif (classes[0] == 3):
                 print("It is yellow signal slowing..")
                 return TrafficLight.YELLOW
              else: return TrafficLight.UNKNOWN
        else:
              return TrafficLight.UNKNOWN
