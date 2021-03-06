from django.conf.urls import patterns, include, url
from django.contrib import admin
from workout_tracker import views

urlpatterns = patterns('',
    
        url(r'^$', views.index, name='index'),
    	url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
    	url(r'^register/(?P<user_type>.+)/$', views.register),
    	url(r'^trainer_info/$', views.provide_trainer_info, name='provide_trainer_info'),
    	url(r'^client_info/$', views.provide_client_info, name='provide_client_info'),
        url(r'^homepage/$', views.homepage, name='homepage'),
    	url(r'^view_pending/$', views.view_pending, name='view_pending'),
    	url(r'^accept/(?P<pid>\d+)$', views.accept, name='accept'),
    	url(r'^reject/(?P<pid>\d+)$', views.reject, name='reject'),
        url(r'^client_workouts/(?P<client_id>\d+)$',views.schedule_trainer, name='client_workouts'),
        url(r'^client_workouts/$',views.schedule_client, name='client_workouts'),
        url(r'^client/(?P<client_id>\d+)$',views.view_client, name='view_client'),
        url(r'^client_bio/(?P<client_id>\d+)$',views.view_client_info, name='view_client_info'),
        url(r'^trainer/(?P<trainer_id>\d+)$', views.view_trainer, name='view_trainer'),
        url(r'^trainer_bio/(?P<trainer_id>\d+)$', views.view_trainer_info, name='view_trainer_info'),
        url(r'^trainers/$', views.trainers, name='trainers'),
        url(r'^clients/$', views.clients, name='clients'),
        url(r'^data/$', views.data, name='data'),
        url(r'^follow/(?P<tid>\d+)$', views.create_follow_request, name='follow'),
        url(r'^friends/$', views.view_clients, name='friends'),
        url(r'^add_workout_trainer/(?P<client_id>\d+)$', views.add_workout_trainer, name='add_workout'),
        url(r'^add_workout/$', views.add_workout, name='add_workout'),
        url(r'^add_exercise/(?P<workout_id>\d+)$', views.add_exercise, name='add_exercise'),
        url(r'^workout_done/(?P<workout_id>\d+)$', views.mark_done, name='workout_done'),
        url(r'^view_exercise/(?P<workout_id>\d+)$', views.view_exercise, name='view_exercise'),
        #url(r'^view_exercise_trainer/(?P<workout_id>\d+)$', views.view_exercise_trainer, name='view_exercise')
        url(r'^edit_info/(?P<u_id>\d+)$',views.edit_info, name='edit_info'),
        url(r'^update/(?P<u_id>\d+)$',views.update, name='update'),
        url(r'^stat/$', views.stat, name='stat')



)
