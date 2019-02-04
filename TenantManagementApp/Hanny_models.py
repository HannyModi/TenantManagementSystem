from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ag_name = models.CharField(max_length=50, unique=True)
    contact_no = models.BigIntegerField(unique=True)
    local_address = models.CharField(max_length=200)
    permenent_address = models.CharField(max_length=200)
    profile_image = models.ImageField(upload_to='profile_images', blank=True)
    ag_email = models.EmailField(max_length=40, unique=True)
    ag_status = models.BooleanField(default=False)
    ad_is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class Tenant(models.Model):
    tn_name = models.CharField(max_length=50)
    tn_contact_no = models.BigIntegerField()
    permenent_address = models.CharField(max_length=200)
    profile_image = models.ImageField(upload_to='profile_images', blank=True)
    tn_document_type = models.CharField(max_length=30)
    tn_document = models.FileField(upload_to='tenant_docs')
    tn_reference_name = models.CharField(max_length=50)
    tn_reference_address = models.CharField(max_length=200)
    # status code: - 1. visit  2.deal Accepted aggrement under process 3.Property handovered 0.Ex-tenant'''
    tn_status = models.IntegerField()
    tn_agent_id = models.ForeignKey('Agent', on_delete=models.CASCADE)
    tn_joining_date = models.DateField(auto_now_add=True)
    tn_is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.tn_name


class Master_Property(models.Model):
    msp_name = models.CharField(max_length=100)
    msp_address = models.CharField(max_length=150)
    msp_description = models.CharField(max_length=200, null=True)
    # false if Property is not allocated to any agent
    msp_status = models.BooleanField(default=False)
    # false if Property is sold out by admin
    msp_is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Master Properties'

    def __str__(self):
        return self.msp_name


class Agent_allocation(models.Model):
    agent = models.ForeignKey('Agent', on_delete=models.CASCADE)
    master_property = models.ForeignKey(
        'Master_Property', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.agent.ag_name + self.master_property.msp_name


class Property(models.Model):
    pr_address = models.CharField(max_length=150)
    pr_rent = models.IntegerField()
    pr_deposite = models.IntegerField()
    master_pr_id = models.ForeignKey(
        'Master_Property', on_delete=models.CASCADE)
    # true if property is provided to any tenant
    pr_is_allocated = models.BooleanField(default=False)
    # false if property is sold out
    pr_isactive = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Properties'

    def __str__(self):
        return self.pr_address


class Property_Visit(models.Model):
    date = models.DateField(default=datetime.date.today)
    tenant = models.ForeignKey('Tenant', on_delete=models.CASCADE)
    visited_property = models.ForeignKey('Property', on_delete=models.CASCADE)
    # 0-Not Intrested, 1-Intrested, 2-Potential Tenant
    tenant_intrest_status = models.IntegerField(null=False)
    
    class Meta:
        verbose_name_plural='Property Visits'
    def __str__(self):
        return str(self.date)


class Property_Allocation(models.Model):
    tenant = models.ForeignKey('Tenant', on_delete=models.CASCADE)
    property_id = models.ForeignKey('Property', on_delete=models.CASCADE)
    agreement_start_date = models.DateField(null=False)
    agreement_end_date = models.DateField(null=False)
    letter_of_acceptence = models.FileField(upload_to='acceptance_letter')
    tenancy_agreement = models.FileField(upload_to='tenancy_agreement')
    final_rent = models.IntegerField(null=False)
    # false for currently not allocated property
    status = models.BooleanField(default=False, null=False)

    class Meta:
        ordering = ('-agreement_start_date',)
        verbose_name_plural='Property Allocation'
    def __str__(self):
        return self.property_id


class Rent_Collection(models.Model):
    property_allocation = models.ForeignKey(
        'Property_Allocation', on_delete=models.CASCADE)
    # reference of hard bill
    receipt_no = models.BigIntegerField()
    # Rent of month
    month = models.IntegerField(max_length=2)
    # rent of year
    year = models.IntegerField(max_length=4)
    date_of_payment = models.DateField(null=False)

    class Meta:
        ordering: ('-date_of_payment',)
        verbose_name_plural='Rent Collections'
    def __str__(self):
        return self.property_allocation
