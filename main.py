
# Na 3
import cv2
from flask import Flask
from flask_restful import Resource, Api

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

app = Flask(__name__)
api = Api(app)


class PeopleCounter(Resource):
    def get(self):

        # load image
        image = cv2.imread('mlodzi-usmiechnieci-ludzie-z-rzedu-na-swiezym-powietrzu_329181-17956.jpg')
        image = cv2.resize(image, (700, 400))

        # detect people in the image
        (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)

        return {'peopleCount': len(rects)}


api.add_resource(PeopleCounter, '/')

if __name__ == '__main__':
    app.run(debug=True)



#Na 4
import cv2
from flask import Flask, request
from flask_restful import Resource, Api
from io import BytesIO

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

app = Flask(__name__)
api = Api(app)


class PeopleCounterStatic(Resource):
    def get(self):
        # load image
        image = cv2.imread('mlodzi-usmiechnieci-ludzie-z-rzedu-na-swiezym-powietrzu_329181-17956.jpg')
        image = cv2.resize(image, (700, 400))

        # detect people in the image
        (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)

        return {'peopleCount': len(rects)}


class PeopleCounterDynamicUrl(Resource):
    def get(self):
        try:
            # 1. Pobrać zdjęcie z otrzymanego adresu
            url = request.args.get('url')
            response = requests.get(url)
            response.raise_for_status()

            # 2. Pobrane zdjęcie można zapisać na dysku lub przetwarzać je w pamięci podręcznej


            # 3. Załadowane zdjęcie do zmiennej image przekazać do algorytmu hog.detectMultiScale i zwrócić z endpointu liczbę wykrytych osób.
            # Detekcja ludzi na zdjęciu
            (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)

            return {'peopleCount': len(rects)}
        except Exception as e:
            return {'error': str(e)}, 500


api.add_resource(PeopleCounterStatic, '/')
api.add_resource(PeopleCounterDynamicUrl, '/dynamic')

if __name__ == '__main__':
    app.run(debug=True)


