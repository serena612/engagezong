from rest_framework import status
from rest_framework.exceptions import APIException


class GameAccountUnavailable(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = 'Game account is missing'
    default_code = 'game_account_unavailable'

class CoinLimitReached(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = 'Coin Limit Reached'
    default_code = 'coin_limit_reached'

class AdLimitReached(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = 'Ad Limit Reached'
    default_code = 'ad_limit_reached'

class SelfAd(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = 'Ad is self owned and thus not rewarded'
    default_code = 'self_ad'

class AdAlreadyClicked(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = 'Ad has already been clicked and can only be rewarded once'
    default_code = 'ad_already_clicked'
    
class MinimumProfileLevelException(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = 'Your profile level is bellow the minimum profile level for this tournament'
    default_code = 'minimum_profile_level'
