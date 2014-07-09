from action_plan.models import*
from datetime import datetime
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import View
from django.shortcuts import  render
from django.views.generic.base import View
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from action_plan.forms import DepartmentForm,ActionPlanForm,DepartmentHeadForm

def home(request):
    return render(request, 'home.html', {})


class Login(View):
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('home'))
        return render(request,'login.html',{})

    def post(self,request,*args,**kwargs):
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user and user.is_active:
            login(request, user)
        else:
            context = {
                'message' : 'Username or password is incorrect'
            }
            return render(request, 'login.html',context)
        context = {
         'Success_message': 'Welcome '+request.POST['username']
        }
        return render(request, 'home.html', context)

class Logout(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('login'))

class DepartmentView(generic.ListView):
    template_name = 'department.html'
    context_object_name = 'latest_department_list'
    def get_queryset(self):
        department = Department.objects.order_by('name')
        return department

class DepartmentHeadView(generic.ListView):
    template_name = 'departmentheads.html'
    context_object_name = 'latest_departmenthead_list'
    def get_queryset(self):
        departmentheads = DepartmentHead.objects.order_by('department')
        return departmentheads

class ActionPlanView(generic.ListView):
    template_name = 'actionplan.html'
    context_object_name = 'latest_actionplan_list'
    def get_queryset(self):
        actionplans = ActionPlan.objects.order_by('date_opened')
        return actionplans

class AddDepartmentView(View):
    def get(self,request,*args,**kwargs):
        if request.method == 'GET':
            form = DepartmentForm()
            return render(request, 'add_departments.html', {"form":form, })

    def post(self,request,*args,**kwargs):
        if request.method == 'POST':
            form = DepartmentForm(request.POST)
            print form
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('department'))

class AddDepartmentHeadView(View):
    def get(self,request,*args,**kwargs):
        if request.method == 'GET':
            form = DepartmentHeadForm()
            return render(request, 'add_departmenthead.html', {"form":form, })

    def post(self,request,*args,**kwargs):
        if request.method == 'POST':
            form = DepartmentHeadForm(request.POST)
            print form
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('departmentheads'))

class AddActionPlanView(View):
    def get(self,request,*args,**kwargs):
        if request.method == 'GET':
            form = ActionPlanForm()
            return render(request, 'add_actionplan.html', {"form":form, })

    def post(self,request,*args,**kwargs):
        if request.method == 'POST':
            form = ActionPlanForm(request.POST)
            print form
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('actionplans'))

class DeleteDepartment(View):
    def get(self,request,*args,**kwargs):
        department_id = kwargs['department_id']
        department = Department.objects.get(id=department_id)
        department.delete()
        return HttpResponseRedirect(reverse('department'))

class DeleteDepartmentHead(View):
    def get(self,request,*args,**kwargs):
        departmenthead_id = kwargs['departmenthead_id']
        departmenthead = DepartmentHead.objects.get(id=departmenthead_id)
        departmenthead.delete()
        return HttpResponseRedirect(reverse('departmenthead'))

class DeleteActionPlan(View):
    def get(self,request,*args,**kwargs):
        actionplan_id = kwargs['actionplan_id']
        actionplan = ActionPlan.objects.get(id=actionplan_id)
        actionplan.delete()
        return HttpResponseRedirect(reverse('actionplans'))

class EditDepartment(View):

    def get(self,request,*args,**kwargs):
        department_id = kwargs['department_id']
        department = Department.objects.get(id=department_id)
        if request.method == 'GET':
            form = DepartmentForm(instance=department)
            context = {
                'form':form,
                'department_id':department_id,
            }
            return render(request,'edit_department.html',context)

    def post(self,request,*args,**kwargs):
        department_id = kwargs['department_id']
        department = Department.objects.get(id=department_id)
        if request.method == 'POST':   
            form = DepartmentForm(request.POST,instance=department)
            form.save()
            return HttpResponseRedirect(reverse('department'))

class EditDepartmentHead(View):

    def get(self,request,*args,**kwargs):
        departmenthead_id = kwargs['departmenthead_id']
        departmenthead = DepartmentHead.objects.get(id=departmenthead_id)
        if request.method == 'GET':
            form = DepartmentHeadForm(instance=departmenthead)
            context = {
                'form':form,
                'departmenthead_id':departmenthead_id,
            }
            return render(request,'edit_department_head.html',context)

    def post(self,request,*args,**kwargs):
        departmenthead_id = kwargs['departmenthead_id']
        departmenthead = DepartmentHead.objects.get(id=departmenthead_id)
        if request.method == 'POST':   
            form = DepartmentHeadForm(request.POST,instance=departmenthead)
            form.save()
            return HttpResponseRedirect(reverse('departmenthead'))

class EditActionPlan(View):

    def get(self,request,*args,**kwargs):
        actionplan_id = kwargs['actionplan_id']
        actionplan = ActionPlan.objects.get(id=actionplan_id)
        if request.method == 'GET':
            form = ActionPlanForm(instance=actionplan)
            context = {
                'form':form,
                'actionplan_id':actionplan_id,
            }
            return render(request,'edit_action_plan.html',context)

    def post(self,request,*args,**kwargs):
        actionplan_id = kwargs['actionplan_id']
        actionplan = ActionPlan.objects.get(id=actionplan_id)
        if request.method == 'POST':   
            form = ActionPlanForm(request.POST,instance=actionplan)
            form.save()
            return HttpResponseRedirect(reverse('actionplans'))