from django.db import models

from behaviour.analysis.emotion_recognition.observer import CONCERNING_EMOTIONS

RESOURCE_TYPES = ["image", "audio", "video", "puzzle"]


class Resource(models.Model):
    type = models.CharField(max_length=500, choices=[(i, i) for i in RESOURCE_TYPES], blank=True, null=True)
    file = models.FileField(upload_to="resources", null=True, blank=True)
    traits = models.TextField(max_length=5000, blank=True, null=True)


class Student(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    dob = models.TextField()
    age = models.IntegerField(default=0)

    traits = models.TextField(max_length=5000, blank=True, null=True)
    preferences = models.TextField(max_length=5000, null=True, blank=True)

    def calculate_age(self):
        year = int(self.dob.split("-")[-1])
        age = 2021 - year
        self.age = age

    def save(self, *args, **kwargs):
        super.save(*args, **kwargs)
        self.calculate_age()


class Soother(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="student")
    resource = models.ForeignKey('students.Resource', on_delete=models.CASCADE, related_name="resource")
    emotion = models.CharField(max_length=10, null=True, blank=True, choices=[(i, i) for i in CONCERNING_EMOTIONS])
    usefulness = models.IntegerField(default=100)     # should be between -100 and 100

    def calculate_usefulness(self, diff=0):
        self.usefulness += diff
        self.save()
