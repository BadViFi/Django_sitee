# from django.db.models.signals import pre_save
# from django.dispatch import receiver

# from .models import Order


# @receiver(pre_save, sender=Order)
# def order_status_changed(sender, instance, **kwargs):
#     if instance.pk:
#         try:
#             old_instance = sender.objects.get(pk=instance.pk)
#         except sender.DoesNotExist:
#             return

#         old_status = dict(Order.STATUS_CHOICES).get(old_instance.status) 
#         new_status = dict(Order.STATUS_CHOICES).get(instance.status)
#         username = instance.user.username
#         if old_status != new_status:
#             from shop_bot import send_telegram_notification
#             send_telegram_notification(old_status, new_status, username)
