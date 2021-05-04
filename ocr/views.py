import glob

from django.core.files.storage import FileSystemStorage
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import UploadSerializer
from banglaocr.settings import MEDIA_URL
import numpy as np
import urllib
import urllib.request
import json
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

from tensorflow import Graph
import cv2
import os

IMAGE_HEIGHT, IMG_WIDTH = 160, 160

model_graph = Graph();
with model_graph.as_default():
    tf_session = tf.compat.v1.Session()
    with tf_session.as_default():
        model = load_model('./models/resnet50-BL.h5')


# ViewSets define the view behavior.
class UploadViewSet(ViewSet):
    serializer_class = UploadSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        myfile = request.FILES['file']
        fs = FileSystemStorage()  # defaults to   MEDIA_ROOT
        cropped_words_folder = os.path.join(MEDIA_URL, "cropped", "words/")
        cropped_letters_folder = os.path.join(MEDIA_URL, "cropped", "letters/")
        # files = glob.glob(cropped_folder2)
        # for f in files:
        #     os.remove(f)
        filename = fs.save(myfile.name, myfile)
        file_url = fs.url(filename)
        f_url = os.path.join(MEDIA_URL, filename)

        test_image = '.' + f_url
        print(test_image)
        # img = cv2.imread(test_image)
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # # Performing OTSU threshold
        # ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        #
        # # Specify structure shape and kernel size.
        # # Kernel size increases or decreases the area
        # # of the rectangle to be detected.
        # # A smaller value like (10, 10) will detect
        # # each word instead of a sentence.
        # rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
        #
        # # Appplying dilation on the threshold image
        # dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
        #
        # # Finding contours
        # contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
        #                                        cv2.CHAIN_APPROX_NONE)
        #
        # # Creating a copy of image
        # im2 = img.copy()
        # count = 0
        # imagePredictions = []
        # for cnt in contours:
        #     x, y, w, h = cv2.boundingRect(cnt)
        #     if w >= 50 and h >= 50:
        #     # Drawing a rectangle on copied image
        #         rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #
        #         # Cropping the text block for giving input to OCR
        #         cropped = im2[y:y + h, x:x + w]
        #         cropped_name = str(count) + '.jpg'
        #         cropped_url = os.path.join(cropped_folder, cropped_name)
        #         cropped_url2 = '.' + cropped_url
        #         ret,thresh = cv2.threshold(cropped, 80, 255, cv2.THRESH_BINARY_INV)
        #
        #         cv2.imwrite(cropped_url2, thresh)
        #         imagePred = image.load_img(cropped_url2, target_size=(IMAGE_HEIGHT, IMG_WIDTH))
        #         input_arr = image.img_to_array(imagePred)
        #
        #         print(input_arr.shape)
        #         input_arr = input_arr/255
        #
        #         print(input_arr.shape)
        #
        #         input_arr2 = input_arr.reshape([1, IMAGE_HEIGHT, IMG_WIDTH, 3])
        #
        #         print(input_arr2.shape)
        #         with model_graph.as_default():
        #             with tf_session.as_default():
        #                 prediction = model.predict(input_arr2)
        #         pred = str(np.argmax(prediction[0]))
        #         imagePredictions.append(pred)
        #         count = count + 1

        # detecing the individual words
        img = cv2.imread(test_image)
        matraless = img.copy()
        matraless_img = self.remove_matra(matraless)
        im2 = img.copy()
        gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

        # ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        # rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
        #
        # # Appplying dilation on the threshold image
        # dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
        #
        # # Finding contours
        # contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        #

        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 30, 150)
        contours, hierarchy = cv2.findContours(matraless_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=self.x_cord_contour, reverse=False)
        # word_count = 0
        letter_count = 0
        imagePredictions = []
        # for cnt in contours:
        #     x, y, w, h = cv2.boundingRect(cnt)
        #     if w >= 200 and h >= 50:
        #         # Cropping the word block
        #         x = x- 20
        #         y = y-20
        #         w = w + 20
        #         h = h + 20
        #
        #         cropped_matraless = matraless_img[y:y + h, x:x + w]
        #         cropped = img[y:y + h, x:x + w]
        #         cropped_name = str(word_count) + '.jpg'
        #         cropped_url = os.path.join(cropped_words_folder, cropped_name)
        #         cropped_url2 = '.' + cropped_url
        #         cv2.imwrite(cropped_url2, cropped_matraless)
        #         word_count = word_count + 1
        #         # gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        #         # blurred = cv2.GaussianBlur(cropped_matraless, (5, 5), 0)
        #         # edged = cv2.Canny(blurred, 30, 150)
        #         contours, hierarchy = cv2.findContours(cropped_matraless.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #         contours = sorted(contours, key=self.x_cord_contour, reverse=False)
        for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                if w >= 10 and h >= 50:
                    # Drawing a rectangle on copied image
                    x = x- 30
                    y = y - 30
                    w = w + 30
                    h = h + 30
                    # rect = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    print (x,y,w,h)

                        # Cropping the text block for giving input to OCR
                    cropped = img[y:y + h, x:x + w]
                    cropped_name = str(letter_count) + '.jpg'
                    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
                    ret, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
                    cropped_url = os.path.join(cropped_letters_folder, cropped_name)
                    cropped_url2 = '.' + cropped_url

                    cv2.imwrite(cropped_url2, binary)
                    imagePred = image.load_img(cropped_url2, target_size=(IMAGE_HEIGHT, IMG_WIDTH))
                    input_arr = image.img_to_array(imagePred)
                    print(input_arr.shape)
                    input_arr = input_arr/255

                    print(input_arr.shape)

                    input_arr2 = input_arr.reshape([1, IMAGE_HEIGHT, IMG_WIDTH, 3])

                    print(input_arr2.shape)
                    with model_graph.as_default():
                        with tf_session.as_default():
                            prediction = model.predict(input_arr2)
                    pred = str(np.argmax(prediction[0]))
                    imagePredictions.append(pred)
                    letter_count = letter_count + 1

        response = {'letterCount':letter_count , 'predictions': imagePredictions}
        return Response(response)

    @staticmethod
    def x_cord_contour(contour):
        # This function take a contour from findContours
        # it then outputs the x centroid coordinates
        M = cv2.moments(contour)
        if M["m00"] != 0:
            return (int(M['m10'] / M['m00']))
        else:
            # set values as what you need in the situation
            return int(0)

    @staticmethod
    def remove_matra(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 75, 150)
        ret, binary = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 80, minLineLength=100, maxLineGap=150)
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(binary, (x1, y1), (x2, y2), (0, 0, 0), 15)
        return binary