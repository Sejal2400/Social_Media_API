from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from.models import User,UserProfile,Post,Follow
from .serializers import UserSerializer,UserProfileSerializer,PostSerializer,UpdatePostSerializer,FollowSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserProfileDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = UserProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_pk = self.kwargs['pk']
        return UserProfile.objects.filter(user__pk=user_pk)
    

class UserUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class =UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)


class CreatePost(generics.CreateAPIView):
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self,serializer):
        serializer.save()

class PostUpdateView(generics.UpdateAPIView):
    serializer_class = UpdatePostSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()

    def perform_update(self,serializer):
        serializer.save(pk=self.request.user.pk,image=self.get_object().image)


class DeletePost(generics.DestroyAPIView):
    serializer_class=PostSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    queryset = Post.objects.all()

    def perform_destroy(self, instance):
        instance.delete()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request,following_user_id):
    try:
        follower_userprofile =  get_object_or_404(UserProfile,user=request.user)
        following_userprofile = get_object_or_404(UserProfile,id=following_user_id)

        if follower_userprofile == following_userprofile:
            return Response({'detail':'You cannot follow yourself'},status=status.HTTP_400_BAD_REQUEST)

        existing_follow = Follow.objects.filter(followers=follower_userprofile,following=following_userprofile).first()
        if existing_follow:
            return Response({'error':"You already following this user"},status=status.HTTP_400_BAD_REQUEST)
        follow=Follow(followers=follower_userprofile,following=following_userprofile)
        follow.save()
        serializer = FollowSerializer(follow)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    except:
        return Response({'error':"Some Issues"},status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request,following_user_id):
    follower_userprofile =  get_object_or_404(UserProfile,user=request.user)
    following_userprofile = get_object_or_404(UserProfile,id=following_user_id)
    existing_follow = Follow.objects.filter(followers=follower_userprofile,following=following_userprofile).first()

    if existing_follow:
        existing_follow.delete()
        return Response({'detail':'You have unfollowed'},status=status.HTTP_200_OK)
    else:
        return Response({'error':"You are not following this user"},status=status.HTTP_400_BAD_REQUEST)