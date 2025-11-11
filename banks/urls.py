
from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.AddBankView.as_view(), name='add_bank'),
    path('<int:bank_id>/branches/add/', views.AddBranchView.as_view(), name='add_branch'),
    path('', views.AllBanksView.as_view(), name='all_banks'),
    path('<int:bank_id>/details/', views.BankDetailsView.as_view(), name='bank_details'),
    path('branch/<int:branch_id>/details/', views.BranchDetailsView.as_view(), name='branch_details'),
    path('branch/<int:branch_id>/edit/', views.EditBranchView.as_view(), name='edit_branch'),
]
