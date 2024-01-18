from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .import views


urlpatterns = [
    path('register/',views.UserRegistrationView.as_view(),name='register'),
    path('token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('retrieve_user_data/<int:pk>/',views.UserProfileDetailView.as_view(),name='retrieve_user_data'),
    path('update_user/<int:pk>/',views.UserUpdateView.as_view(),name='update_user') ,
    path('create-post/',views.CreatePost.as_view(),name='create-post'),
    path('update-post/<int:pk>/',views.PostUpdateView.as_view(),name='update-post'),
    path('delete-post/<int:pk>/',views.DeletePost.as_view(),name='delete-post'),
    path('follow-user/<int:following_user_id>/',views.follow_user,name='follow-user'),
    path('unfollow-user/<int:following_user_id>/',views.unfollow_user,name='unfollow-user')

]