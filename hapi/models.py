from email.policy import default

from django.db import models

# Create your models here.
NULL_BLANK = {
    "null": True,
    "blank": True
}

class NPIPractitioner(models.Model):
    npi_name = models.CharField(max_length=120, **NULL_BLANK)
    family_name = models.CharField(max_length=120, **NULL_BLANK)
    gender = models.CharField(max_length=120, **NULL_BLANK)
    dob = models.DateTimeField(**NULL_BLANK)
    mobile = models.CharField(max_length=120, **NULL_BLANK)
    email = models.CharField(max_length=120, **NULL_BLANK)
    address1 = models.CharField(max_length=120, **NULL_BLANK)
    city = models.CharField(max_length=120, **NULL_BLANK)
    state = models.CharField(max_length=120, **NULL_BLANK)
    pincode = models.CharField(max_length=120, **NULL_BLANK)
    epic_npi_id = models.CharField(max_length=120, **NULL_BLANK)
    epic_response = models.JSONField(**NULL_BLANK)
    created_at = models.DateTimeField(auto_now_add=True, **NULL_BLANK)
    modified_on = models.DateTimeField(auto_now=True, **NULL_BLANK)

class Patient(models.Model):
    name = models.CharField(max_length=120, **NULL_BLANK)
    family_name = models.CharField(max_length=120, **NULL_BLANK)
    gender = models.CharField(max_length=120, **NULL_BLANK)
    dob = models.DateTimeField(**NULL_BLANK)
    mobile = models.CharField(max_length=120, **NULL_BLANK)
    email = models.CharField(max_length=120, **NULL_BLANK)
    address1 = models.CharField(max_length=120, **NULL_BLANK)
    city = models.CharField(max_length=120, **NULL_BLANK)
    state = models.CharField(max_length=120, **NULL_BLANK)
    pincode = models.CharField(max_length=120, **NULL_BLANK)
    epic_pid = models.CharField(max_length=120, **NULL_BLANK)
    epic_response = models.JSONField(**NULL_BLANK)
    created_at = models.DateTimeField(auto_now_add=True, **NULL_BLANK)
    modified_on = models.DateTimeField(auto_now=True, **NULL_BLANK)
    npi = models.ForeignKey(NPIPractitioner, on_delete=models.SET_NULL, **NULL_BLANK)


class InsuranceOrganization(models.Model):
    epic_org_id = models.CharField(max_length=120, **NULL_BLANK)
    org_name = models.CharField(max_length=120, **NULL_BLANK)
    address_line = models.CharField(max_length=120, **NULL_BLANK)
    city = models.CharField(max_length=120, **NULL_BLANK)
    state = models.CharField(max_length=120, **NULL_BLANK)
    country = models.CharField(max_length=120, **NULL_BLANK)
    pincode = models.CharField(max_length=120, **NULL_BLANK)
    org_mobile = models.CharField(max_length=120, **NULL_BLANK)
    org_email = models.CharField(max_length=120, **NULL_BLANK)
    epic_resp_id = models.CharField(max_length=120, **NULL_BLANK)
    epic_response = models.JSONField(**NULL_BLANK)
    created_at = models.DateTimeField(auto_now_add=True, **NULL_BLANK)
    modified_on = models.DateTimeField(auto_now=True, **NULL_BLANK)


class Coverage(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE, **NULL_BLANK)
    org_id = models.ForeignKey(InsuranceOrganization, on_delete=models.CASCADE, **NULL_BLANK)
    amount = models.IntegerField(default=0)
    plan = models.CharField(max_length=120, **NULL_BLANK)
    balance = models.IntegerField(default=0)
    start_date = models.DateTimeField(**NULL_BLANK)
    end_date = models.DateTimeField(**NULL_BLANK)
    epic_resp_id = models.CharField(max_length=120, **NULL_BLANK)
    epic_response = models.JSONField(**NULL_BLANK)
    created_at = models.DateTimeField(auto_now_add=True, **NULL_BLANK)
    modified_on = models.DateTimeField(auto_now=True, **NULL_BLANK)


class Claims(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE, **NULL_BLANK)
    org_id = models.ForeignKey(InsuranceOrganization, on_delete=models.CASCADE, **NULL_BLANK)
    npi_id = models.ForeignKey(NPIPractitioner, on_delete=models.CASCADE, **NULL_BLANK)
    coverage_id = models.ForeignKey(Coverage, on_delete=models.SET_NULL, **NULL_BLANK)
    claim_type = models.CharField(max_length=120, **NULL_BLANK)
    unit_price = models.IntegerField(default=0)
    net_amount = models.IntegerField(default=0)
    claim_amount = models.IntegerField(default=0)
    currency = models.CharField(max_length=120, **NULL_BLANK)
    status = models.BooleanField(default=False)
    epic_resp_id = models.CharField(max_length=120, **NULL_BLANK)
    epic_response = models.JSONField(**NULL_BLANK)
    created_at = models.DateTimeField(auto_now_add=True, **NULL_BLANK)
    modified_on = models.DateTimeField(auto_now=True, **NULL_BLANK)