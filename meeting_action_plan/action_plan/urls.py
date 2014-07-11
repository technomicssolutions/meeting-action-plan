from django.conf.urls import patterns,url
from django.contrib.auth.decorators import login_required
from action_plan.views import*
urlpatterns = patterns('',
	url(r'login/$',  Login.as_view(), name='login'),
    url(r'logout/$', Logout.as_view(), name='logout'),
    url(r'^$', Home.as_view(), name='home'),
    url(r'add_department/$',  login_required(AddDepartmentView.as_view()), name='add_department'),
    url(r'department/$',login_required(DepartmentView.as_view()),name='department'),
    url(r'users/$',login_required (UserView.as_view()),name='users'),
    url(r'actionplans/$',login_required(ActionPlanView.as_view()),name='actionplans'),
    url(r'add_user/$',login_required(AddUserView.as_view()), name='add_user'),
    
    url(r'add_actionplan/$',login_required(AddActionPlanView.as_view()), name='add_actionplan'),
    url(r'deletedepartment/(?P<department_id>\d+)/$',login_required(DeleteDepartment.as_view()), name='deletedepartment'),
    url(r'deleteuser/(?P<user_id>\d+)/$',login_required(DeleteUser.as_view()), name='deleteuser'),
    url(r'delete_action_plan/(?P<actionplan_id>\d+)/$',login_required(DeleteActionPlan.as_view()), name='delete_action_plan'),
   	url(r'editdepartment/(?P<department_id>\d+)/$', login_required(EditDepartment.as_view()), name='editdepartment'),
   	url(r'edituser/(?P<user_id>\d+)/$',login_required(EditUser.as_view()), name='edituser'),
    url(r'editactionplan/(?P<actionplan_id>\d+)/$',login_required(EditActionPlan.as_view()), name='editactionplan'),
    )