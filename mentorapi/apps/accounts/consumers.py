import logging
import json

from channels.consumer import SyncConsumer
from django.forms.models import model_to_dict
from djoser.compat import get_user_email
from djoser.email import ActivationEmail, PasswordResetEmail

from apps.accounts.models import Profile

logger = logging.getLogger('email')


class AccountBackgroundTasks(SyncConsumer):

    def send_activation_email(self, context):
        user = context.get('user')
        request = context.get('request')
        to = [get_user_email(user)]
        ActivationEmail(request, {'user': user}).send(to)

    def send_password_reset_email(self, context):
        user = context.get('user')
        request = context.get('request')
        to = [get_user_email(user)]
        PasswordResetEmail(request, {'user': user}).send(to)

    def calculate_profile_percentage(self, context):
        print("arrived here successfully", context)
        fields = {'full_name': 10, 'age': 10, 'city': 10, 'address': 10}
        completed_profile_percent = 0
        try:
            user = json.loads(context.get('user'))[0].get('pk')
            profile_instance = model_to_dict(Profile.objects.get(user=user))
            print('profile get_instance', profile_instance)
            for field in profile_instance:
                print ("field", field)
                if fields.get(field) is not None:
                    print("field found", field)
                    completed_profile_percent += fields[field]
        except Profile.DoesNotExist:
            logger.error("Profile does not exist")
        print("completed_profile_percent", completed_profile_percent)
        return completed_profile_percent
