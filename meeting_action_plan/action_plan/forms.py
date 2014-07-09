from action_plan.models import *
from django.forms import ModelForm
from django import forms

class DepartmentForm(ModelForm):
	class Meta:

		model = Department
		fields = ['name']

class DepartmentHeadForm(ModelForm):
	class Meta:

		model = DepartmentHead
		fields = ['department', 'user']

class ActionPlanForm(ModelForm):
	class Meta:

		model = ActionPlan
		fields = ['action', 'focal', 'priority', 'status', 'comments', 'department']