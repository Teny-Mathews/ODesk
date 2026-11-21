"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.urls import path
from buildings import views

urlpatterns = [
    path('listcreate',views.BuildingListCreateView.as_view(), name='building_list_create'),
    path('detailview/<int:pk>/',views.BuildingDetailView.as_view(), name='building_detail'),

    path('<int:building_id>/offices/',views.OfficeSpaceListCreateView.as_view(), name='office_list_create'),
    path('<int:building_id>/offices/<int:pk>/',views.OfficeSpaceDetailView.as_view(), name='office_detail'),

    path('<int:building_id>/images/',views.BuildingImageListCreateView.as_view(), name='building_image_list_create'),
    path('<int:building_id>/images/<int:pk>/',views.BuildingImageDetailView.as_view(),name='building_image_detail'),

    path('<int:building_id>/offices/<int:office_id>/images/',views.OfficeImageListCreateView.as_view(),name='office_image_list_create'),
    path('<int:building_id>/offices/<int:office_id>/images/<int:pk>/',views.OfficeImageDetailView.as_view(),name='office_image_detail'),

    path('amenities/',views.AmenityListCreateView.as_view(), name='amenity_list_create'),

    path('<int:pk>/amenities/',views.BuildingAmenityView.as_view(), name='building_amenities'),

    path('<int:building_id>/offices/<int:office_id>/amenities/',views.OfficeAmenityView.as_view(), name='office_amenities'),

    path('browse/', views.BuildingBrowseView.as_view(), name='building_browse'),

    path('browse/<int:pk>/',views.BuildingBrowseDetailView.as_view(), name='building_browse_detail'),

    path('offices/browse/',views.OfficeBrowseView.as_view(), name='office_browse'),

    path('offices/browse/<int:pk>/',views.OfficeBrowseDetailView.as_view(), name='office_browse_detail'),
]