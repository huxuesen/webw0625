from task.utils.notification.mail_notification import MailNotification
from task.utils.notification.wechat_notification import WechatNotification
from task.utils.notification.bark_notification import BarkNotification
from task.utils.notification.custom_notification import CustomNotification

import logging
logger = logging.getLogger('main')


def new_handler(name):
    if name == 'custom':
        return CustomNotification()
    elif name == 'bark':
        return BarkNotification()
    elif name == 'mail':
        return MailNotification()
    elif name == 'wechat':
        return WechatNotification()
    else:
        logger.error('通知方式错误')
        raise Exception('通知方式错误')
