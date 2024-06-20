"""
URL configuration for spoid project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get_table_data/', GetTableData.as_view()),
    path('login/', include('login.urls')),
    path('component_detail/', ComponentDetail.as_view()),
    path('create_order/', CreateOrder.as_view()),
    path('create_user/', CreateUser.as_view()),
    path('detail_order/', DetailOrder.as_view()),
    path('get_order_list/', GetOrder.as_view()),
    path('get_component_list/', GetComponentList.as_view()),
]
