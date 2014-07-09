from django.conf.urls import patterns,url
from action_plan import views
urlpatterns = patterns('',
	url(r'login/$', views.Login.as_view(), name='login'),
    url(r'logout/$',views.Logout.as_view(), name='logout'),
    url(r'^$', 'action_plan.views.home', name='home'),
    url(r'^department/$',views.DepartmentView.as_view(),name='department'),
    url(r'^departmentheads/$',views.DepartmentHeadView.as_view(),name='departmentheads'),
    url(r'^actionplans/$',views.ActionPlanView.as_view(),name='actionplans'),
    url(r'add_departments/$', views.AddDepartmentView.as_view(), name='add_departments'),
    url(r'add_departmenthead/$', views.AddDepartmentHeadView.as_view(), name='add_departmenthead'),
    url(r'add_actionplan/$', views.AddActionPlanView.as_view(), name='add_actionplan'),
    url(r'^deletedepartment/(?P<department_id>\d+)/$', views.DeleteDepartment.as_view(), name='deletedepartment'),
    url(r'^deletedepartmenthead/(?P<departmenthead_id>\d+)/$', views.DeleteDepartmentHead.as_view(), name='deletedepartmenthead'),
    url(r'^delete_action_plan/(?P<actionplan_id>\d+)/$', views.DeleteActionPlan.as_view(), name='delete_action_plan'),
   	url(r'^editdepartment/(?P<department_id>\d+)/$', views.EditDepartment.as_view(), name='editdepartment'),
   	url(r'^editdepartmenthead/(?P<departmenthead_id>\d+)/$', views.EditDepartmentHead.as_view(), name='editdepartmenthead'),
    url(r'^editactionplan/(?P<actionplan_id>\d+)/$', views.EditActionPlan.as_view(), name='editactionplan'),
    )