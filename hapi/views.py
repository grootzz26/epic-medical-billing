from os import error

from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
import requests
from rest_framework.response import Response
from rest_framework import status
import json
from .models import *
from main.settings import FHIR_CONF
import datetime


BASE_URL = FHIR_CONF["baseURL"]


def make_request(url, method, body=None, params=None, headers=None):
    if method.lower() == "get":
        resp = requests.get(url, params=params, headers=headers)
    else:
        resp = requests.post(url, params=params, data=body, headers=headers)
    return resp

class PatientCreateAPIView(ListCreateAPIView):

    def create(self, request, *args, **kwargs):
        breakpoint()
        data = json.loads(request.body.decode("utf-8"))
        breakpoint()
        body_frame = {
                "resourceType": "Patient",
                "name": [
                    {
                        "use": "official",
                        "given": [data["name"]],
                        "family": data.get("family_name", "")
                    }
                ],
                "gender": data["gender"],
                "birthDate": data["dob"],
                "telecom": [
                    {
                        "value": data["mobile"],
                        "use": "mobile",
                        "system": "phone"
                    },
                    {
                        "system": "email",
                        "value": data["email"]
                    }
                ],
                "address": [
                    {
                        "line": [
                            data["address1"]
                        ],
                        "city": data["city"],
                        "state": data["state"],
                        "postalCode": data["pincode"]
                    }
                ]
            }
        url = BASE_URL + "Patient"
        header = {}
        header["content-Type"] = "application/json"
        try:
            resp = make_request(url, "POST", body=json.dumps(body_frame), headers=header)
            if resp.status_code == 201:
                result = resp.json()
                Patient.objects.create(epic_pid=result["id"], epic_response=result, **data)
                return Response(data=result, status=status.HTTP_201_CREATED)
            else:
                return Response(data=resp.json(), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("@@@@@@@@@@@@@@@: ", e)
            return Response(data=False, status=status.HTTP_400_BAD_REQUEST)


class PatientsAPIView(ListCreateAPIView):

    def list(self, request, *args, **kwargs):
        pid = kwargs.get("pid")
        try:
            if pid:
                url = BASE_URL + "Patient/" + str(pid)
                resp = make_request(url, "GET")
                return Response(data=resp.json(), status=status.HTTP_200_OK)
            patients = Patient.objects.all()
            data = []
            for patient in patients:
                url = BASE_URL + "Patient/" + str(patient.epic_pid)
                resp = make_request(url, "GET")
                data.append(resp.json())
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            print("@@@@@@@@@@@@@@@: ", e)
            return Response(data=False, status=status.HTTP_400_BAD_REQUEST)


class OrganisationAPIView(ListCreateAPIView):

    def list(self, request, *args, **kwargs):
        pid = kwargs.get("pid")
        try:
            if pid:
                url = BASE_URL + "Organization/" + pid
                resp = make_request(url, "GET")
                return Response(data=resp.json(), status=status.HTTP_400_BAD_REQUEST)
            patients = InsuranceOrganization.objects.all()
            data = []
            for patient in patients:
                url = BASE_URL + "Organization/"+ str(patient.epic_resp_id)
                resp = make_request(url, "GET")
                data.append(resp.json())
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            print("@@@@@@@@@@@@@@@: ", e)
            return Response(data=False, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8"))
        payload = {
              "resourceType": "Organization",
              "id": data["epic_org_id"],
              "name": data["org_name"],
              "type": [
                {
                  "coding": [
                    {
                      "system": "http://terminology.hl7.org/CodeSystem/organization-type",
                      "code": "ins",
                      "display": "Insurance Company"
                    }
                  ]
                }
              ],
              "address": [
                {
                  "line": [data["address_line"]],
                  "city": data["city"],
                  "state": data["state"],
                  "postalCode": data["pincode"],
                  "country": data["country"]
                }
              ],
              "telecom": [
                {
                  "system": "phone",
                  "value": data["org_mobile"],
                  "use": "work"
                },
                {
                  "system": "email",
                  "value": data["org_email"],
                  "use": "work"
                }
              ]
            }
        url = BASE_URL + "Organization"
        header = {}
        header["content-Type"] = "application/json"
        try:
            resp = make_request(url, "POST", body=json.dumps(payload), headers=header)
            if resp.status_code == 201:
                result = resp.json()
                InsuranceOrganization.objects.create(epic_resp_id=result["id"], epic_response=result, **data)
                return Response(data=result, status=status.HTTP_201_CREATED)
            else:
                return Response(data=resp.json(), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("@@@@@@@@@@@@@@@: ", e)
            return Response(data=False, status=status.HTTP_400_BAD_REQUEST)


class NPIGetCreateAPIView(ListCreateAPIView):

    def list(self, request, *args, **kwargs):
        pid = kwargs.get("pid")
        try:
            if pid:
                url = BASE_URL + "Practitioner/" + pid
                resp = make_request(url, "GET")
                return Response(data=resp.json(), status=status.HTTP_400_BAD_REQUEST)
            npi_data = NPIPractitioner.objects.all()
            data = []
            for npi in npi_data:
                url = BASE_URL + "Practitioner/"+ str(npi.epic_npi_id)
                resp = make_request(url, "GET")
                data.append(resp.json())
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            print("@@@@@@@@@@@@@@@: ", e)
            return Response(data=False, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8"))
        payload = {
            "resourceType": "Practitioner",
            "identifier": [
                {
                    "system": "http://hl7.org/fhir/sid/us-npi",
                    "value": "1234567893"
                }
            ],
            "active": True,
            "name": [
                {
                    "use": "official",
                    "family": data["family_name"],
                    "given": [data["npi_name"]]
                }
            ],
            "telecom": [
                {
                    "system": "phone",
                    "value": data["mobile"],
                    "use": "work"
                }
            ],
            "address": [
                {
                    "use": "work",
                    "line": [data["address1"]],
                    "city": data["city"],
                    "state": data["state"],
                    "postalCode": data["pincode"]
                }
            ]
        }

        url = BASE_URL + "Practitioner"
        header = {}
        header["content-Type"] = "application/json"
        try:
            resp = make_request(url, "POST", body=json.dumps(payload), headers=header)
            breakpoint()
            if resp.status_code == 201:
                result = resp.json()
                NPIPractitioner.objects.create(epic_npi_id=result["id"], epic_response=result, **data)
                return Response(data=result, status=status.HTTP_201_CREATED)
            else:
                return Response(data=resp.json(), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("@@@@@@@@@@@@@@@: ", e)
            return Response(data=False, status=status.HTTP_400_BAD_REQUEST)


class CoverageAPIView(ListCreateAPIView):

    def list(self, request, *args, **kwargs):
        pid = kwargs.get("pid")
        try:
            if pid:
                url = BASE_URL + "Coverage/" + pid
                resp = make_request(url, "GET")
                return Response(data=resp.json(), status=status.HTTP_400_BAD_REQUEST)
            npi_data = Coverage.objects.all()
            data = []
            for npi in npi_data:
                url = BASE_URL + "Coverage/" + str(npi.epic_resp_id)
                resp = make_request(url, "GET")
                data.append(resp.json())
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            print("@@@@@@@@@@@@@@@: ", e)
            return Response(data=False, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8"))
        payload = {
            "resourceType": "Coverage",
            "status": "active",
            "type": {
            "coding": [
              {
                "system": "http://terminology.hl7.org/CodeSystem/coverage-type",
                "code": "EHCPOL"
              }
            ]
            },
            "subscriber": {
                "reference": f"Patient/{data['patient_id']}"
            },
            "payor": [
                {
                  "reference": f"Organization/{data['insurance_company_id']}"
                }
            ],
            "policyHolder": {
                "reference": f"Patient/{data['patient_id']}"
            },
            "beneficiary": {
                "reference": f"Patient/{data['patient_id']}"
            },
            "class": [
                        {
                            "type": {
                                "coding": [
                                    {
                                        "system": "http://terminology.hl7.org/CodeSystem/coverage-class",
                                        "code": "benefit",
                                        "display": "Coverage Amount"
                                    }
                                ]
                            },
                            "value": data["coverage_amount"],
                            "name": "Annual Benefit Limit"
                        }
                    ],
            "period": {
                "start": "2024-01-01",
                "end": "2024-12-31"
            }
        }
        url = BASE_URL + "Coverage"
        header = {}
        header["content-Type"] = "application/json"
        try:
            resp = make_request(url, "POST", body=json.dumps(payload), headers=header)
            if resp.status_code == 201:
                result = resp.json()
                date_dict = {
                    "start_date": datetime.datetime.strptime(data["start_date"], "%Y-%m-%d"),
                    "end_date": datetime.datetime.strptime(data["end_date"], "%Y-%m-%d")
                }
                Coverage.objects.create(epic_resp_id=result["id"], epic_response=result, patient_id=Patient.objects.get(epic_pid=data["patient_id"]),
                                        org_id=InsuranceOrganization.objects.get(epic_resp_id=data["insurance_company_id"]), amount=data["coverage_amount"],
                                        plan=data["plan"], **date_dict)
                return Response(data=result, status=status.HTTP_201_CREATED)
            else:
                return Response(data=resp.json(), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("@@@@@@@@@@@@@@@: ", e)
            return Response(data=False, status=status.HTTP_400_BAD_REQUEST)

class ClaimAPIView(ListCreateAPIView):

    def create(self, request, *args, **kwargs):
        coverage_id = kwargs["coverage_id"]
        try:
            coverage = Coverage.objects.get(epic_resp_id=coverage_id)
        except Exception as err:
            return
        data = json.loads(request.body.decode("utf-8"))
        patient_id = coverage.patient_id.epic_pid
        org_id = coverage.org_id.epic_resp_id
        npi = coverage.patient_id.npi.epic_npi_id
        coverage_id = coverage_id
        payload = {
            "resourceType": "Claim",
            "identifier": [
                {
                    "system": "http://example.org/claim-ids",
                    "value": "claim12345"
                }
            ],
            "status": "active",
            "type": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/claim-type",
                        "code": data["claim_type"]
                    }
                ]
            },
            "use": "claim",
            "patient": {
                "reference": f"Patient/{patient_id}"
            },
            "created": "2025-01-13",
            "insurer": {
                "reference": f"Organization/{org_id}"
            },
            "provider": {
                "reference": f"Practitioner/{npi}"
            },
            "priority": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/processpriority",
                        "code": "normal"
                    }
                ]
            },
            "payee": {
                "type": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/payeetype",
                            "code": "provider"
                        }
                    ]
                }
            },
            "coverage": [
                {
                    "sequence": 1,
                    "focal": True,
                    "coverage": {
                        "reference": f"Coverage/{coverage_id}"
                    }
                }
            ],
            "item": [
                {
                    "sequence": 1,
                    "productOrService": {
                        "coding": [
                            {
                                "system": "http://example.org/codes/services",
                                "code": "exam"
                            }
                        ]
                    },
                    "unitPrice": {
                        "value": data["unit_price"],
                        "currency": data["currency"]
                    },
                    "net": {
                        "value": data["net_amount"],
                        "currency": data["currency"]
                    }
                }
            ],
            "total": {
                "value": data["claim_amount"],
                "currency": data["currency"]
            }
        }

        url = BASE_URL + "Claim"
        header = {}
        header["content-Type"] = "application/json"
        try:
            resp = make_request(url, "POST", body=json.dumps(payload), headers=header)
            if resp.status_code == 201:
                result = resp.json()
                Claims.objects.create(epic_resp_id=result["id"], epic_response=result,
                                        patient_id=coverage.patient_id,
                                        org_id=coverage.org_id, npi_id=coverage.patient_id.npi, **data)
                return Response(data=result, status=status.HTTP_201_CREATED)
            else:
                return Response(data=resp.json(), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("@@@@@@@@@@@@@@@: ", e)
            return Response(data=False, status=status.HTTP_400_BAD_REQUEST)

