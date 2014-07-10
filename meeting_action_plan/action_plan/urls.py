from django.conf.urls import patterns,url
from action_plan.views import*
urlpatterns = patterns('',
	url(r'login/$',  Login.as_view(), name='login'),
    url(r'logout/$', Logout.as_view(), name='logout'),
    url(r'^$', Home.as_view(), name='home'),
    url(r'department/$', DepartmentView.as_view(),name='department'),
    url(r'users/$', UserView.as_view(),name='users'),
    url(r'actionplans/$', ActionPlanView.as_view(),name='actionplans'),
    url(r'add_user/$',  AddUserView.as_view(), name='add_user'),
    url(r'add_department/$',  AddDepartmentView.as_view(), name='add_department'),
    url(r'add_actionplan/$',  AddActionPlanView.as_view(), name='add_actionplan'),
    url(r'deletedepartment/(?P<department_id>\d+)/$',  DeleteDepartment.as_view(), name='deletedepartment'),
    url(r'deleteuser/(?P<user_id>\d+)/$',  DeleteUser.as_view(), name='deleteuser'),
    url(r'delete_action_plan/(?P<actionplan_id>\d+)/$',  DeleteActionPlan.as_view(), name='delete_action_plan'),
   	url(r'editdepartment/(?P<department_id>\d+)/$',  EditDepartment.as_view(), name='editdepartment'),
   	url(r'edituser/(?P<user_id>\d+)/$',  EditUser.as_view(), name='edituser'),
    url(r'editactionplan/(?P<actionplan_id>\d+)/$',  EditActionPlan.as_view(), name='editactionplan'),
    )