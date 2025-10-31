from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .models import Person
import face_recognition
import numpy as np

# ✅ 1. REGISTER VIEW
def register(request):
    if request.method == 'POST' and request.FILES.get('image'):
        name = request.POST['name']
        image = request.FILES['image']

        fs = FileSystemStorage()
        file_path = fs.save(image.name, image)
        image_path = fs.path(file_path)

        # Load and encode face
        img = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(img)

        if encodings:
            encoding = encodings[0].tobytes()
            Person.objects.create(name=name, encoding=encoding)
            return render(request, 'attendance/register.html', {'success': True})
        else:
            return render(request, 'attendance/register.html', {'error': 'No face detected!'})

    return render(request, 'attendance/register.html')


# ✅ 2. RECOGNIZE VIEW
def recognize(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']

        fs = FileSystemStorage()
        file_path = fs.save(image.name, image)
        image_path = fs.path(file_path)

        # Load image to recognize
        img = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(img)

        if not encodings:
            return render(request, 'attendance/recognize.html', {'error': 'No face detected!'})

        face_encoding = encodings[0]
        persons = Person.objects.all()

        for person in persons:
            known_encoding = np.frombuffer(person.encoding)
            matches = face_recognition.compare_faces([known_encoding], face_encoding)
            if True in matches:
                return render(request, 'attendance/recognize.html', {'name': person.name})

        return render(request, 'attendance/recognize.html', {'error': 'No match found!'})

    return render(request, 'attendance/recognize.html')
