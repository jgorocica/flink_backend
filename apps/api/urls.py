from django.urls import path
from apps.api.views import CompanyList, CompanyDetail

urlpatterns = [
    path('', CompanyList.as_view()),
    path('<uuid:id>/', CompanyDetail.as_view()),
]