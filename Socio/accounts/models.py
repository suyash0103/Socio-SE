from django.db import models
from django.conf import settings
import numpy as np
User=settings.AUTH_USER_MODEL
import base64, face_recognition




class Face(models.Model):
    user = models.OneToOneField(User,primary_key=True, on_delete=models.CASCADE)
    face_encoding = models.BinaryField(null=True)

    def __str__(self):
        return str(self.user) + "'s face"

    def get_face_encoding(self):
        return np.frombuffer(base64.decodebytes(self.face_encoding))
    #
    # def set_face_encoding(self):
    #     picture = face_recognition.load_image_file(str(self.face_image))
    #     face_encoding = face_recognition.face_encodings(picture)[0]
    #     self.face_encoding = base64.b64encode(face_encoding)
