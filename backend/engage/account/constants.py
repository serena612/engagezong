from common.mixins import LabelChoices


class Gender(LabelChoices):
    MALE = 'male', 'Male'
    FEMALE = 'female', 'Female'


class FriendStatus(LabelChoices):
    ACCEPTED = 'accepted', 'Accepted'
    DECLINED = 'declined', 'Declined'
    PENDING = 'pending', 'Pending'


class CoinTransaction(LabelChoices):
    ADD = 'add', 'Add'
    BUY = 'buy', 'Buy'
    SEND = 'send', 'Send',
    RECEIVE = 'receive', 'Receive'
    REDEEM = 'redeem', 'Redeem',
    PAY = 'pay','Pay Fee'
    RETRIEVE = 'retrieve','Retrieve'
    REFER = 'refer', 'Refer'
    AD_CLICK = 'ad_click', 'Ad Click'
    AD_VIEW = 'ad_view', 'Ad View'
    ENGAGE_VIEW = 'engage_view', 'Engage View'

class Transaction(LabelChoices):
    ADD = 'add', 'Add'
    BUY = 'buy', 'Buy Coins'
    SEND = 'send', 'Send Coins',
    RECEIVE = 'receive', 'Receive Coins'
    REDEEM = 'redeem', 'Redeem',
    PAY = 'pay','Pay Fee',
    NOTIFICATION_CLAIM = 'notification','Notification Claim',
    RETRIEVE = 'retrieve','Retrieve'
    REFER = 'refer', 'Refer'
    AD_CLICK = 'ad_click', 'Ad Click'
    AD_VIEW = 'ad_view', 'Ad View'
    ENGAGE_VIEW = 'engage_view', 'Engage View'


class NotificationType(LabelChoices):
    WEB = 'web', 'Web'
    MOBILE = 'mobile', 'Mobile'


class SubscriptionPlan(LabelChoices):
    FREE = 'free', 'Free'
    PAID1 = 'paid1', 'Paid 1'
    PAID2 = 'paid2', 'Paid 2'
    PAID3 = 'paid3', 'Paid 3'
    DAILY = 'daily', 'Daily'
    WEEKLY = 'weekly', 'Weekly'
    MONTHLY = 'Monthly', 'monthly'

class SubscriptionPackages(LabelChoices):
    FREE = 'free', 'Free'
    PAID1 = 'daily', 'Daily'
    PAID2 = 'weekly', 'Weekly'
    PAID3 = 'Monthly', 'monthly'


class SectionLog(LabelChoices):
    TOURNAMENT = 'tournaments', 'tournaments'
    GAME = 'games', 'games'
    PRIZE = 'prizes', 'prizes'
    REDEEM = 'redeem', 'redeem'
    WINNERS = 'winners', 'winners'
