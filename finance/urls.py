from . import views
from django.urls import path
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as a_views

app_name='finance'

urlpatterns=[
    path('register',views.register,name='register'),
    path('login/',a_views.LoginView.as_view(template_name='finance/login.html'),name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('transaction_form/',views.form,name='transaction_form'),
    path('transaction_list/',views.transaction_list,name='transaction_list'),
    path('edit/<int:id>/',views.update_transaction,name='update'),
    path('delete/<int:id>/',views.deleteform,name='delete'),
    path('',views.dashboard,name='dashboard'),
    path('export/csv/',views.export_transactions_csv,name='export_csv')
]