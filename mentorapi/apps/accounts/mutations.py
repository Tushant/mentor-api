from django.contrib.auth.tokens import default_token_generator

from djoser.conf import settings as djoser_settings
from djoser.utils import decode_uid

import graphene

from rest_framework_jwt.serializers import (
    JSONWebTokenSerializer,
    RefreshJSONWebTokenSerializer
)

from .models import (User as UserModel, Profile, Experience,
                     Skill, Language, Education, Achievement)
from .schema import (User, ProfileNode)
from .input import (ProfileInput, ExperienceInput, SkillInput,
                    LanguageInput, EducationInput, AchievementInput)
from .serializers import PasswordResetConfirmRetypeSerializer
from .utils import send_activation_email, send_password_reset_email


class Register(graphene.Mutation):
    """
    Mutation to register a user
    """
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        password_repeat = graphene.String(required=True)
        role = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, email, password, password_repeat, role):
        if password == password_repeat:
            try:
                user = UserModel.objects.create(
                    email=email,
                    role=role,
                    is_active=False
                )
                user.set_password(password)
                user.save()
                if djoser_settings.get('SEND_ACTIVATION_EMAIL'):
                    send_activation_email(user, info.context)
                return Register(success=bool(user.id))
            # TODO: specify exception
            except Exception:
                errors = ["email", "Email already registered."]
                return Register(success=False, errors=errors)
        errors = ["password", "Passwords don't match."]
        return Register(success=False, errors=errors)


class Activate(graphene.Mutation):
    """
    Mutation to activate a user's registration
    """
    class Arguments:
        token = graphene.String(required=True)
        uid = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, token, uid):

        try:
            uid = decode_uid(uid)
            user = UserModel.objects.get(pk=uid)
            if not default_token_generator.check_token(user, token):
                return Activate(success=False, errors=['stale token'])
                pass
            user.is_active = True
            user.save()
            return Activate(success=True, errors=None)

        except Exception:
            return Activate(success=False, errors=['unknown user'])


class Login(graphene.Mutation):
    """
    Mutation to login a user
    """
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    token = graphene.String()
    user = graphene.Field(User)

    def mutate(self, info, email, password):
        user = {'email': email, 'password': password}
        serializer = JSONWebTokenSerializer(data=user)
        if serializer.is_valid():
            token = serializer.object['token']
            user = serializer.object['user']
            print ('user', user)
            return Login(success=True, user=user, token=token, errors=None)
        else:
            return Login(
                success=False,
                token=None,
                errors=['email', 'Unable to login with provided credentials.']
            )


class RefreshToken(graphene.Mutation):
    """
    Mutation to reauthenticate a user
    """
    class Arguments:
        token = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    token = graphene.String()

    def mutate(self, info, token):
        serializer = RefreshJSONWebTokenSerializer(data={'token': token})
        if serializer.is_valid():
            return RefreshToken(
                success=True,
                token=serializer.object['token'],
                errors=None
            )
        else:
            return RefreshToken(
                success=False,
                token=None,
                errors=['email', 'Unable to login with provided credentials.']
            )


class ResetPassword(graphene.Mutation):
    """
    Mutation for requesting a password reset email
    """

    class Arguments:
        email = graphene.String(required=True)

    success = graphene.Boolean()

    def mutate(self, info, email):
        try:
            user = User.objects.get(email=email)
            send_password_reset_email(info.context, user)
            return ResetPassword(success=True)
        except Exception:
            return ResetPassword(success=True)


class ResetPasswordConfirm(graphene.Mutation):
    """
    Mutation for requesting a password reset email
    """

    class Arguments:
        uid = graphene.String(required=True)
        token = graphene.String(required=True)
        email = graphene.String(required=True)
        new_password = graphene.String(required=True)
        re_new_password = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, uid, token, email, new_password, re_new_password):
        serializer = PasswordResetConfirmRetypeSerializer(data={
            'uid': uid,
            'token': token,
            'email': email,
            'new_password': new_password,
            're_new_password': re_new_password,
        })
        if serializer.is_valid():
            serializer.user.set_password(serializer.data['new_password'])
            serializer.user.save()
            return ResetPasswordConfirm(success=True, errors=None)
        else:
            return ResetPasswordConfirm(
                success=False, errors=[serializer.errors])


class DeleteAccount(graphene.Mutation):
    """
    Mutation to delete an account
    """
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, email, password):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ['unauthenticated']
        elif is_authenticated and not email == info.context.user.email:
            errors = ['forbidden']
        elif not info.context.user.check_password(password):
            errors = ['wrong password']
        else:
            info.context.user.delete()
            return DeleteAccount(success=True)
        return DeleteAccount(success=False, errors=errors)

# class SocialLogin(graphene.Mutation):
#     """ Mutation to login through social app """
#     social_auth = graphql_social_auth.SocialAuth.Field()

#  PROFILE RELATED


class ProfileMutation(graphene.Mutation):
    class Arguments:
        input = ProfileInput(description="These fields are required", required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    profile = graphene.Field(ProfileNode)

    @staticmethod
    def mutate(self, info, **args):
        print ('info', args, info.context.user, info.context.FILES, info.context.FILES.get('avatar', None))
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ['unauthenticated']
            return ProfileMutation(success=False, errors=errors)
        else:
            profile = Profile.objects.get(user=UserModel.objects.get(id=info.context.user))
            profile.full_name = args.get('input').get('full_name', None)
            profile.age = args.get('input').get('age', None)
            profile.city = args.get('input').get('city', None)
            profile.address = args.get('input').get('address', None)
            profile.name_of_company = args.get('input').get('name_of_company', None)
            profile.job_title = args.get('input').get('job_title', None)
            profile.zip_code = args.get('input').get('zip_code', None)
            profile.slogan = args.get('input').get('slogan', None)
            profile.bio = args.get('input').get('bio', None)
            profile.website = args.get('input').get('website', None)
            profile.github = args.get('input').get('github', None)
            profile.linkedin = args.get('input').get('linkedin', None)
            profile.twitter = args.get('input').get('twitter', None)
            profile.facebook = args.get('input').get('facebook', None)
            profile.save()
            return ProfileMutation(profile=profile, success=True, errors=None)


class ExperienceMutation(graphene.Mutation):
    class Arguments:
        input = ExperienceInput()
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    @staticmethod
    def mutate(self, info, **args):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ["unauthenticated"]
            return ExperienceMutation(success=False, errors=errors)
        else:
            experience = Profile.objects.get(user=UserModel.objects.get(id=info.context.user))
            experience.title = args.get('input').get('title', None)
            experience.name_of_company = args.get('input').get('name_of_company', None)
            experience.location = args.get('input').get('location', None)
            experience.start_date = args.get('input').get('start_date', None)
            experience.end_date = args.get('input').get('end_date', None)
            experience.save()
            return ExperienceMutation(experience=experience, success=True, errors=None)


class SkillMutation(graphene.Mutation):
    class Arguments:
        input = SkillInput()
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    @staticmethod
    def mutate(self, info, **args):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ["unauthenticated"]
            return SkillMutation(success=False, errors=errors)
        else:
            skill = Profile.objects.get(user=UserModel.objects.get(id=info.context.user))
            skill.title = args.get('input').get('title', None)
            skill.save()
            return SkillMutation(skill=skill, success=True, errors=None)


class LanguageMutation(graphene.Mutation):
    class Arguments:
        input = LanguageInput()
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    @staticmethod
    def mutate(self, info, **args):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ["unauthenticated"]
            return LanguageMutation(success=False, errors=errors)
        else:
            language = Profile.objects.get(user=UserModel.objects.get(id=info.context.user))
            language.name = args.get('input').get('name', None)
            language.save()
            return LanguageMutation(language=language, success=True, errors=None)


class EducationMutation(graphene.Mutation):
    class Arguments:
        input = EducationInput()
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    @staticmethod
    def mutate(self, info, **args):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ["unauthenticated"]
            return EducationMutation(success=False, errors=errors)
        else:
            education = Profile.objects.get(user=UserModel.objects.get(id=info.context.user))
            education.title = args.get('input').get('title', None)
            education.sub_title = args.get('input').get('sub_title', None)
            education.start_date = args.get('input').get('start_date', None)
            education.end_date = args.get('input').get('end_date', None)
            education.save()
            return EducationMutation(education=education, success=True, errors=None)


class AchievementMutation(graphene.Mutation):
    class Arguments:
        input = AchievementInput()
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    @staticmethod
    def mutate(self, info, **args):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ["unauthenticated"]
            return AchievementMutation(success=False, errors=errors)
        else:
            achievement = Profile.objects.get(user=UserModel.objects.get(id=info.context.user))
            achievement.category = args.get('input').get('category', None)
            achievement.title = args.get('input').get('title', None)
            achievement.sub_title = args.get('input').get('sub_title', None)
            achievement.description = args.get('input').get('description', None)
            achievement.save()
            return AchievementMutation(achievement=achievement, success=True, errors=None)
