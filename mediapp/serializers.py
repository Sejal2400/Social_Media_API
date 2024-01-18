from rest_framework import serializers
from .models import User,UserProfile,Post,Follow
 

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('biography','profile_pic')


class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()
    class Meta:
        model = User
        fields = ('id','username','email','first_name','last_name','userprofile','password')
        extra_kwargs={
            'password':{'write_only':True}  #for password not to be shown in response.
        }

    def create(self,validated_data):
        profile_data = validated_data.pop('userprofile') #profile pc, bio
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user,**profile_data)
        return user
    
    def update(self,instance,validated_data):
        profile_data = validated_data.pop('userprofile')
        instance.email = validated_data.get('email',instance.email)
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)

        password = validated_data.get('password')
        if password:
            instance.set_password('password')


        instance.save()

        #Updateuser profile

        userprofile = instance.userprofile
        userprofile.biography = profile_data.get('biography',userprofile.biography)
        userprofile.profile_pic = profile_data.get('profile_pic',userprofile.profile_pic)
        userprofile.save()

        return instance
    
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields =('id','user','content','image','created_at')

class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields =('id','user','content','created_at')

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields ='__all__'