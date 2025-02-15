from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('account/', views.account_view, name='account'),  # Updated path
    path('trash/', views.trash_view, name='trash'),
    path('version-control/', views.version_control, name='version_control'),
    path('generate-subject-line/', views.generate_subject_line, name='generate_subject_line'),
    path('save-edited-subject/', views.save_edited_subject, name='save_edited_subject'),
    path('get-subject/<int:subject_id>/', views.get_subject, name='get_subject'),
    path('get-subject-lines/', views.get_subject_lines, name='get_subject_lines'),
    path('generate-reply-email-write/', views.generate_reply_email_writer, name='generate_reply_email_writer'),
    path('save-edited-reply/', views.save_edited_reply, name="save_edited_reply"),
    path('email-generation/',views.generate_email, name='email-generation'),
    path('subject-generation/',views.generate_subject, name='subject-generation'),
    path('reply-email-generation/',views.generate_reply_email, name='reply-email-generation'),
    path('get-saved-replies/', views.get_saved_replies, name='get_saved_replies'),
]
