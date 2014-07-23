from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User

PRIORITY_CHOICES  =(
            ('1','one'),
            ('2','two'),
            ('3','three'),
    )
STATUS_CHOICES =(
            ('Open','Open'),
            ('Closed','Closed'),
    )
class Department(models.Model):

    name = models.CharField('Department Name', max_length=200, unique=True)
    head = models.ForeignKey(User, null=True, blank=True)
    def __unicode__(self):
        return self.name


class ActionPlan(models.Model):

    date_opened = models.DateTimeField('Date Opened',null=True,blank=True)
    action = models.TextField('Requirement/Action', null=True, blank=True)
    focal = models.CharField('Focal', max_length=200, null=True, blank=True)
    priority = models.CharField( max_length=1, choices=PRIORITY_CHOICES)
    status = models.CharField( max_length=10, choices=STATUS_CHOICES)
    date_closed = models.DateTimeField('Date Closed', null=True, blank=True)
    target_date = models.DateTimeField('Target Date', null=True, blank=True)
    comments = models.TextField('Comments/Update', null=True, blank=True)
    department = models.ForeignKey(Department, null=True, blank=True)

    def __unicode__(self):
        return self.department.name 