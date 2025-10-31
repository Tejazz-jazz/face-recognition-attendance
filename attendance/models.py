from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=100)
    encoding = models.BinaryField()  # Stores the face encoding (as bytes)
    image = models.ImageField(upload_to='faces/', null=True, blank=True)

    def __str__(self):
        return self.name
