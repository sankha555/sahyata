from django.db import models

from dbms.api.behaviour.models import Trait, Resource


class Student(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    dob = models.DateField()
    age = models.IntegerField(default=0)

    traits = models.ManyToManyField(related_name="traits")


class Soother(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE, related_name="student")
    resource = models.ForeignKey("Resource", on_delete=models.CASCADE, related_name="resource")
    usefulness = models.IntegerField(default=0)     # should be between -100 and 100

