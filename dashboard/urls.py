from django.urls import path, include
from . import views

urlpatterns = [
	path('api/controls/', views.ControlList.as_view(), name='controls_list'),
	path('api/controls/<int:pk>', views.ControlDetail.as_view(), name='controls_detail'),
	path('', views.index, name='index')
]
