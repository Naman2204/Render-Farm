from django.urls import path

from . import views

urlpatterns = [
    path("", views.base_page_route, name="base"),
    path("api/suggestions", views.suggestions_page_route, name="suggestions"),
    path("api/signin", views.signin_page_route, name="signin"),
    path("signup", views.signup_page_route, name="signup"),
    path("upload/", views.upload_page_route, name="upload"),
    path("logout/", views.logout_page_route, name="logout"),
    path("about/", views.about_page_route, name="about"),
]
