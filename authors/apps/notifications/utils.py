class NotificationPermissions:
    RECEIVE_NOTIFICATION_EMAILS = 'RECEIVE_NOTIFICATION_EMAILS'
    FOLLOWED_AUTHOR_ARTICLE_CREATED = 'FOLLOWED_AUTHOR_ARTICLE_CREATED'
    PROFILE_FOLLOW = 'PROFILE_FOLLOW'
    MY_ARTICLE_COMMENTED = 'MY_ARTICLE_COMMENTED'
    FAVORITED_ARTICLE_COMMENTED = 'FAVORITED_ARTICLE_COMMENTED'
    MY_ARTICLE_LIKED = 'MY_ARTICLE_LIKED'
    FAVORITED_ARTICLE_LIKED = 'FAVORITED_ARTICLE_LIKED'
    AUTHORED_ARTICLE_COMMENTED = 'AUTHORED_ARTICLE_COMMENTED'
    AUTHORED_ARTICLE_LIKED = 'AUTHORED_ARTICLE_LIKED'
    AUTHORED_ARTICLE_FAVORITED = 'AUTHORED_ARTICLE_FAVORITED'

    @classmethod
    def all(cls):
        return {
            'RECEIVE_NOTIFICATION_EMAILS': cls.RECEIVE_NOTIFICATION_EMAILS,
            'FOLLOWED_AUTHOR_ARTICLE_CREATED':
            cls.FOLLOWED_AUTHOR_ARTICLE_CREATED,
            'PROFILE_FOLLOW': cls.PROFILE_FOLLOW,
            'MY_ARTICLE_COMMENTED': cls.MY_ARTICLE_COMMENTED,
            'FAVORITED_ARTICLE_COMMENTED': cls.FAVORITED_ARTICLE_COMMENTED,
            'MY_ARTICLE_LIKED': cls.MY_ARTICLE_LIKED,
            'FAVORITED_ARTICLE_LIKED': cls.FAVORITED_ARTICLE_LIKED,
            'AUTHORED_ARTICLE_COMMENTED': cls.AUTHORED_ARTICLE_COMMENTED,
            'AUTHORED_ARTICLE_LIKED': cls.AUTHORED_ARTICLE_LIKED,
            'AUTHORED_ARTICLE_FAVORITED': cls.AUTHORED_ARTICLE_FAVORITED
         }

    def get_all(self):
        return list(self.all().keys())


permissions = NotificationPermissions()
