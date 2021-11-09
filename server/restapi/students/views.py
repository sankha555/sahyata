from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from server.restapi.students.models import Student, Soother, Resource, Trait


class StudentRegistrationView(APIView):
    def post(self, request, format=None):
        data = request.data

        new_student = Student.objects.create(
            name=data["name"],
            dob=data["dob"],
            preferences=data["preferences"]
        )
        new_student.save()

        res = {
            "name": new_student.name,
            "age": new_student.age,
        }

        return Response(res, status=status.HTTP_201_CREATED)


class ResourceCreationView(APIView):
    def post(self, request, format = None):
        data = request.data
        files = request.files

        resource = Resource(
            type=data["type"],
            file=files["file"],
        )
        resource.save()
