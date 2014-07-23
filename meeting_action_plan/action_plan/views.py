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
from action_plan.forms import DepartmentForm,ActionPlanForm
from django.db import IntegrityError
from django.db import transaction, DatabaseError

class Home(View):
    def get(self,request):
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
        return HttpResponseRedirect(reverse('actionplans'))

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

class UserView(generic.ListView):
    template_name = 'users.html'
    context_object_name = 'latest_user_list'
    def get_queryset(self):
        users = User.objects.order_by('username').exclude(is_superuser=True)
        return users

class ActionPlanView(View):
    def get(self, request, *args, **kwargs):
        actionplans_opened= ActionPlan.objects.filter(status='Open').order_by('target_date')
        actionplans_closed= ActionPlan.objects.filter(status='Closed').order_by('-date_closed')
        context = { 
            'actionplans_opened':actionplans_opened,
            'actionplans_closed':actionplans_closed,
        }
        return render(request,'actionplan.html',context)

class AddDepartmentView(View):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(request, 'add_department.html', {'users': users})
    def post(self, request, *args, **kwargs):
        users = User.objects.all()
        try:
            department = Department.objects.get(name=request.POST['name'])
            
            context = {'users': users, 'message': 'Department name already exists'}
            context.update(request.POST)
            return render(request, 'add_department.html', context)
        except:
            
            user_id=request.POST['user_id']
            if request.POST['name'] !='' and request.POST['name'] !=None and len(request.POST['name']) > 0:
                department = Department() 
                department.name = request.POST['name']
                if user_id != 'None': 
                    user = User.objects.get(id=user_id)       
                    department.head = user
                department.save()
            else:
                return render(request, 'add_department.html', {'message':'Department name is null','users': users, })
        return HttpResponseRedirect(reverse('departments'))

class AddUserView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'add_user.html',{})
    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=request.POST['username'])
            context = {
                'message': 'Sorry..This username already exists'
            }
            return render(request, 'add_user.html',context)
        except:
            user = User()
            if request.POST['username'] !='':
                user.username = request.POST['username']
                user.first_name = User(request.POST['firstname'])
                user.last_name = User(request.POST['lastname'])
                user.save()
                user.set_password(request.POST['password'])
                user.save()    
                return HttpResponseRedirect(reverse('users'))
            else:
                return render(request, 'add_user.html',{'message':'Username is blank'})

class AddActionPlanView(View):
    def get(self,request,*args,**kwargs):
        departments = Department.objects.all()
        plan = ActionPlan.objects.all()
        if request.method == 'GET':
            
            formplan = ActionPlanForm()
            context ={
                'plan':plan,
                'departments':departments,
                'formplan':formplan,
            }
            return render(request, 'add_actionplan.html', context)

    def post(self,request,*args,**kwargs):
        if request.method == 'POST':
            form = ActionPlanForm(request.POST)
            departments = Department.objects.all()
            plan = ActionPlan.objects.all()
            
            if form.is_valid():
                form.save()
                if request.user.is_superuser:
                    department_id = request.POST['department_id']
                    department = Department.objects.get(id=department_id)
                    plan = ActionPlan.objects.latest('id')
                    plan.department = department
                    plan.save()
                else :
                    department_name = request.POST['department_name']
                    department = Department.objects.get(name=department_name)
                    plan = ActionPlan.objects.latest('id')
                    plan.department =department
                    plan.save()
                if plan.status == 'Open':
                    plan.date_opened = datetime.now()
                else:
                    plan.date_closed = datetime.now()
                plan.save()

                return HttpResponseRedirect(reverse('actionplans'))
            
            context ={
                'plan':plan,
                'departments':departments,
                'formplan':form,
            }
            return render(request, 'add_actionplan.html', context)
class DeleteDepartment(View):
    def get(self,request,*args,**kwargs):
        department_id = kwargs['department_id']
        department = Department.objects.get(id=department_id)
        department.delete()
        return HttpResponseRedirect(reverse('departments'))

class DeleteUser(View):
    def get(self,request,*args,**kwargs):
        user_id = kwargs['user_id']
        user = User.objects.get(id=user_id)

        user.delete()
        return HttpResponseRedirect(reverse('users'))

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
        users = User.objects.all()
        if request.method == 'GET':
            context = {
                'users':users,
                'department':department,
                'department_id':department_id,
            }
            return render(request,'edit_department.html',context)

    def post(self,request,*args,**kwargs):

        department_id = kwargs['department_id']
        department = Department.objects.get(id=department_id)
        user_id=request.POST['user_id']
        users = User.objects.all()
        if request.method == 'POST': 
            try:  
                department.name = request.POST['name']
                department.save()
                if request.POST['name'] !='':
                    if user_id != 'None':
                        head = User.objects.get(id=user_id)       
                        department.head = head
                    department.save()
                    return HttpResponseRedirect(reverse('departments'))
                else :
                    return render(request, 'edit_department.html',{'department_id':department_id,'department':department,'users':users,'message':'Department name is blank'})
            except DatabaseError:
                try:
                    transaction.rollback()
                except transaction.TransactionManagementError:
                    users = User.objects.all()
            context = {'users' : users,'department_id':department_id, 'department':department, 'message':'Department name ' + request.POST['name']+ ' already exists'}
            return render(request ,'edit_department.html',context)

        

class EditUser(View):

    def get(self,request,*args,**kwargs):
        user_id = kwargs['user_id']
        users = User.objects.get(id=user_id)
        if request.method == 'GET':
            context = {
                'users':users,
                'user_id':user_id,
            }
            return render(request,'edit_user.html',context)
    def post(self, request, *args, **kwargs):
        user_id = kwargs['user_id']
        user = User.objects.get(id=user_id)
        try:
            if request.POST['username'] !='':
                user.username = request.POST['username']
                user.first_name = User(request.POST['firstname'])
                user.last_name = User(request.POST['lastname'])
                user.save()
                return HttpResponseRedirect(reverse('users'))
            else:
                return render(request, 'edit_user.html',{'users':user,'user_id':user_id ,'message':'Username is blank'})
        except DatabaseError:
            try:
                transaction.rollback()
            except transaction.TransactionManagementError:
                user = User.objects.get(id=user_id)
                user.save()
        context = {'users' : user,'user_id':user_id, 'message':'username already exists'}
        return render(request ,'edit_user.html',context)
            

class EditActionPlan(View):

    def get(self,request,*args,**kwargs):
        actionplan_id = kwargs['actionplan_id']
        actionplan = ActionPlan.objects.get(id=actionplan_id)
        if request.method == 'GET':
            form = ActionPlanForm(instance=actionplan)
            context = {
                'form':form,
                'actionplan_id':actionplan_id,
                'actionplan':actionplan,
            }
            return render(request,'edit_action_plan.html',context)

    def post(self,request,*args,**kwargs):
        actionplan_id = kwargs['actionplan_id']
        actionplan = ActionPlan.objects.get(id=actionplan_id)
        if request.method == 'POST':
            form = ActionPlanForm(request.POST,instance=actionplan)
            if form.is_valid():
                form.save()
                if request.POST['status'] == 'Closed':
                    actionplan.date_closed = datetime.now()
                actionplan.save();
                return HttpResponseRedirect(reverse('actionplans'))
           
        return render(request,'edit_action_plan.html',{'form':form, 'actionplan_id':actionplan_id, })

    