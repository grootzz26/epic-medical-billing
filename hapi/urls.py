from django.urls import path
from .views import *

urlpatterns = [
    path("patient/create/", PatientCreateAPIView.as_view(), name="patient_create"),
    path("patient/all/", PatientsAPIView.as_view(), name="patients_data"),
    path("patient/<str:pid>/", PatientsAPIView.as_view(), name="patient_id_get"),
    path("organisation/", OrganisationAPIView.as_view(), name="organisation"),
    path("organisation/<str:pid>/", OrganisationAPIView.as_view(), name="organisation"),
    path("coverage/", CoverageAPIView.as_view(), name="coverage"),
]