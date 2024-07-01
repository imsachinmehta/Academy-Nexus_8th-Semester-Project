from django.urls import path

from . import views
from . import marketplaceViews

urlpatterns = [
    path("", views.home, name="home-page"),
    path("register/", views.register, name="register"),
    path("signin/", views.signin, name="signin"),
    path("signout/", views.signout, name="signout"),
    path("post<id>/", views.view_post, name="view-post"),
    path("addcomment<id>/",views.add_comment, name="add-comment"),
    path("marketplace/", marketplaceViews.marketPlace, name="market-place"),
    path("addproduct/", marketplaceViews.add_product, name="add-product"),
    path("deleteproduct<id>/", marketplaceViews.delete_product, name="delete-product"),
    path("services/", views.services, name="services"),
    path("services/delete<id>/", views.delete_service, name="delete-service"),
    path("addservice/", views.add_service, name="add-service"),
    path("addpost/", views.add_post, name="add-post"),
    path("deletepost<id>/", views.delete_post, name="delete-post"),
    path("profile/", views.profile, name="profile"),
    path("addskill/", views.add_new_skill, name="add-skill"),
    path("skill/",views.assign_skill, name="assign-skill"),
    path("updateprofile/", views.update_profile_pic, name="update-profile-pic"),
]
