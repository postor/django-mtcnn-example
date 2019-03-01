import web
import json
import numpy as np
import cv2
from mtcnn.mtcnn import MTCNN
import io

detector = MTCNN()


urls = ('/', 'Upload')

class Upload:
    def GET(self):
        return """<html><head></head><body>
<form method="POST" enctype="multipart/form-data" action="">
<input type="file" name="file" />
<br/>
<input type="submit" />
</form>
</body></html>"""

    def POST(self):
        x = web.input(file={})
        print( x['file'].file.name)

        buffer = io.BytesIO(x['file'].file.read()).getbuffer()
        image = cv2.imdecode(np.frombuffer(buffer, np.uint8), -1)
        
        result = detector.detect_faces(image)
        web.header('Content-Type', 'application/json')
        return json.dumps({'results':result})


if __name__ == "__main__":
   app = web.application(urls, globals()) 
   app.run()