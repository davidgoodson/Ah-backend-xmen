from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from authors.apps.utils.custom_permissions.permissions import \
    if_owner_permission
from authors.apps.utils.messages import error_messages, response

from authors.apps.authentication.models import User
from .models import Profile, ProfileManager
from .renderers import (UserProfileJSONRenderer, UserProfileListRenderer,
    ReadStatsJsonRenderer
)
from .serializers import (ProfileListSerializer, ProfileUpdateSerializer,
                          UserProfileSerializer)

from authors.apps.notifications.backends import notify
from authors.apps.articles.models import ReadStats
from authors.apps.articles.serializers import ReadStatsSerializer

class UserProfileView(generics.RetrieveAPIView):
    """ Fetches and displays the details
    of a user profile to the currently
    logged in person
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer
    renderer_classes = (UserProfileJSONRenderer, )

    def get_serializer_context(self):
        return {
            'request': self.request
        }

    def get_object(self, *args, **kwargs):
        username = self.kwargs.get("username")
        return get_object_or_404(Profile, user__username=username)


class UserProfileUpdateView(generics.UpdateAPIView):
    """ Allows the currently logged in user
    to edit their user profile
    possible editable fields include,
    first_name, last_name, bio
    and image """
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated, ]
    
    def get_object(self):
       
        if_owner_permission(self.request, **self.kwargs)
        username = self.kwargs.get("username")
        obj = get_object_or_404(Profile, user__username=username)
        return obj

class UserProfileListView(generics.ListAPIView):
    serializer_class = ProfileListSerializer
    permission_classes = [IsAuthenticated,]
    renderer_classes = [UserProfileListRenderer,]

    def get_queryset(self):
        return Profile.objects.all()

class FollowView(generics.GenericAPIView):
    """
    Allows the currently logged in user to follow and unfollow 
    profiles of other users
    """
    permission_classes = [IsAuthenticated,]
    renderer_classes = (UserProfileJSONRenderer, )

    def post(self, request, *args, **kwargs):
        author_username = self.kwargs.get('username')
        Profile.objects.follow_author(request.user, author_username)
        notify.profile_followed(request,Profile.objects.get(user__username=author_username))
        return Response({'message':response['follow message'].format(author_username)},status=status.HTTP_200_OK)

    def delete(self, *args, **kwargs):
        author_to_unfollow = self.kwargs.get('username')
        Profile.objects.unfollow_author(self.request.user, author_to_unfollow)
        return Response({'message':response['unfollow message'].format(author_to_unfollow)},status=status.HTTP_200_OK)


class FollowersView(generics.ListAPIView):
    """
    This class returns a list of profiles for 
    followers of a given user. 
    """
    serializer_class = ProfileListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]
    renderer_classes = [UserProfileListRenderer,]


    def fetch_profiles(self,users):
        for user in users:
            yield user.profile

    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return  self.fetch_profiles(user.profile.followers.all())

class FollowingView(generics.ListAPIView):
    """
    This class returns a list of profiles
    a given user is following.
    """
    serializer_class = ProfileListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]
    renderer_classes = [UserProfileListRenderer,]

    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return  user.is_following.all()


class ReadStatsView(generics.ListAPIView):
    """
    Function returning the list of articles read by one user
    """
    serializer_class = ReadStatsSerializer
    permission_classes = [IsAuthenticated,]
    renderer_classes = [ReadStatsJsonRenderer,]

    def get_queryset(self, *args, **kwargs):

        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        read_stats = ReadStats.objects.all().filter(user=user)
        return [item.article for item in read_stats]

    def get(self, request, username):

        last_read_articles = -10
        if username == request.user.username:
            articles = self.get_queryset()
            last_read_article_list = [{'title':article.title,
                                          'slug':article.slug,
                                          'author':article.author.user.username} 
                                          for article in articles[last_read_articles:]]
            data = {
                'user': request.user.username,
                'total_articles_read': len(articles),
                'recent_articles_read': list(reversed(last_read_article_list))
            }
            return Response(data)
        else:
            return Response({
                'error_message': 'You dont have the permissions to access this route'
            }, status=status.HTTP_403_FORBIDDEN)

