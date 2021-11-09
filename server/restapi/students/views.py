from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from server.restapi.students.models import Student, Soother, Resource


class StudentRegistrationView(APIView):
    @staticmethod
    def post(self, request, format=None):
        data = request.data

        new_student = Student.objects.create(
            name=data["name"],
            dob=data["dob"],
            traits=data["traits"],
            preferences=data["preferences"]
        )
        new_student.save()

        res = {
            "name": new_student.name,
            "age": new_student.age,
        }

        return Response(res, status=status.HTTP_201_CREATED)


class ResourceCreationView(APIView):
    @staticmethod
    def post(self, request, format=None):
        data = request.data
        files = request.files

        resource = Resource.objects.create(
            type=data["type"],
            file=files["file"],
            traits=files["traits"]
        )
        resource.save()


class ResourceDownloadView(APIView):
    @staticmethod
    def get(self, request, pk):
        resource = Resource.objects.get(pk=pk)

        file = resource.file
        file.open(mode='rb')
        content = file.readlines()
        file.close()

        res = {
            "type": resource.type,
            "filename": file.name,
            "content": content,
        }

        return Response(res, status=status.HTTP_200_OK)


class SootherView(APIView):
    @staticmethod
    def post(self, request):
        data = request.data

        student = Student.objects.get(pk=data["student_pk"])
        resource = Resource.objects.get(pk=data["resource_pk"])

        soother = Soother.objects.create(
            student=student,
            resource=resource,
            emotion=int(data["emotion"])
        )
        soother.save()

        res = {
            "resourcePath": "",
        }

        return Response(res, status=status.HTTP_201_CREATED)

    @staticmethod
    def put(self, request):
        data = request.data

        soother = Soother.objects.get(pk=data["pk"])
        soother.calculate_usefulness(diff=float(data["diff"]))

        return Response({"msg": "OK"}, status=status.HTTP_200_OK)


class DecisionsView(APIView):
    @staticmethod
    def get(self, request):
        data = request.data

        student = Student.objects.get(pk=data["student_pk"])

        soothers = list(Soother.objects.filter(student=student, emotion=data["emotion"]).exclude(usefulness__gt=0).order_by('-usefulness'))
        soothers = [{
            "resource_pk": s.resource.pk
        } for s in soothers]

        prospective_resources = []
        resources = Resource.objects.all()
        for r in resources:
            if data["emotion"] in r.traits:
                prospective_resources.append({
                    "resource_pk": r.pk
                })

        res = {
            "soothers": soothers,
            "resources": prospective_resources,
        }

        return Response(res, status=status.HTTP_200_OK)

