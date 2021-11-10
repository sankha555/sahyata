from django.urls import path, include

from server.restapi.students.views import *

urlpatterns = [
    path('student/registration', StudentRegistrationView, name='student_registration'),

    path('resource/creation', ResourceCreationView, name='resource_creation'),

    path('resource', ResourceDownloadView, name='resource_download'),

    path('soother', ResourceCreationView, name='soother'),

    path('decisions', DecisionsView, name='decisions')
]