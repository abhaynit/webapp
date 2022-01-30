from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.


BRANCH_CHOICES = (
    ('CSE','CSE'),
    ('CIVIL','CIVIL'),
    ('EEE','EEE'),
    ('EIE','EIE'),
    ('ECE','ECE'),
    ('MECH','MECH'),
)

class recrd(models.Model):
    student_id = models.BigIntegerField()
    student_name = models.CharField(max_length=100)
    student_branch = models.CharField(choices=BRANCH_CHOICES,max_length=10)
    purpose = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    exit_time = models.DateTimeField(default=datetime.datetime.now,blank=True)
    entry_time = models.DateTimeField(null=True,blank=True)
    is_late = models.BooleanField(default=False)

