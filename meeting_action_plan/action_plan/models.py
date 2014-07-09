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
            ('O','Open'),
            ('C','Closed'),
	)
class Department(models.Model):

	name = models.CharField('Department Name', max_length=200, unique=True)

	def __unicode__(self):
	 	return self.name

class DepartmentHead(models.Model):

	user = models.ForeignKey(User, null=True, blank=True)
	department = models.ForeignKey(Department, null=True, blank=True)

	def __unicode__(self):
		return self.department.name + ' - ' + self.user.first_name

class ActionPlan(models.Model):

	date_opened = models.DateTimeField('Date Opened', auto_now_add=True)
	action = models.TextField('Requirement/Action', null=True, blank=True)
	focal = models.CharField('Focal', max_length=200, null=True, blank=True)
	priority = models.CharField( max_length=1, choices=PRIORITY_CHOICES)
	status = models.CharField( max_length=5, choices=STATUS_CHOICES)
	date_closed = models.DateField('Date Closed', auto_now_add=True)
	comments = models.TextField('Comments/Update', null=True, blank=True)
	department = models.ForeignKey(Department, null=True, blank=True)

	def __unicode__(self):
		return self.department.name 