from rest_framework.throttling import UserRateThrottle


class PostCreationRateThrottle(UserRateThrottle):
    """
    This class handles the throttling of the number of posts created by a user.
    """
    scope = 'user_new_post_creation'


class CommentCreationRateThrottle(UserRateThrottle):
    """
    This class handles the throttling of the number of comments created by a user.
    """
    scope = 'user_new_comment_creation'
