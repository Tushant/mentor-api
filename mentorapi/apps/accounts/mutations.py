from django.contrib.auth.tokens import default_token_generator

from djoser.conf import settings as djoser_settings
from djoser.utils import decode_uid

import graphene

from rest_framework_jwt.serializers import (
    JSONWebTokenSerializer,
    RefreshJSONWebTokenSerializer
)

from core.utils import get_instance
from .models import (User as UserModel, Profile, Experience,
                     Skill, Language, Education, Achievement)
from .schema import (User, ProfileNode, ExperienceNode, SkillNode,
                     LanguageNode, EducationNode, AchievementNode)
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


class CreateProfile(graphene.Mutation):
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
            return CreateProfile(success=False, errors=errors)
        else:
            profile = Profile.objects.create(
                 user=info.context.user,
                 full_name=args.get('input').get('full_name', None),
                 age=args.get('input').get('age', None),
                 city=args.get('input').get('city', None),
                 address=args.get('input').get('address', None),
                 name_of_company=args.get('input').get('name_of_company', None),
                 job_title=args.get('input').get('job_title', None),
                 zip_code=args.get('input').get('zip_code', None),
                 slogan=args.get('input').get('slogan', None),
                 bio=args.get('input').get('bio', None),
                 website=args.get('input').get('website', None),
                 github=args.get('input').get('github', None),
                 linkedin=args.get('input').get('linkedin', None),
                 twitter=args.get('input').get('twitter', None),
                 facebook=args.get('input').get('facebook', None))
            return CreateProfile(profile=profile, success=True, errors=None)


class UpdateProfile(graphene.Mutation):
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
            return UpdateProfile(success=False, errors=errors)
        else:
            profile = Profile.objects.get(user=info.context.user)
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
            return UpdateProfile(profile=profile, success=True, errors=None)


class CreateExperience(graphene.Mutation):
    class Arguments:
        input = ExperienceInput(description="These fields are required", required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    experience = graphene.Field(ExperienceNode)

    @staticmethod
    def mutate(self, info, **args):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ['unauthenticated']
            return CreateExperience(success=False, errors=errors)
        else:
            profile = Profile.objects.get(user=info.context.user)
            experience = Experience.objects.create(
                 profile=profile,
                 title=args.get('input').get('title', None),
                 name_of_company=args.get('input').get('name_of_company', None),
                 location=args.get('input').get('location', None),
                 start_date=args.get('input').get('start_date', None),
                 end_date=args.get('input').get('end_date', None),
                 )
            return CreateExperience(experience=experience, success=True, errors=None)


class UpdateExperience(graphene.Mutation):
    class Arguments:
        input = ExperienceInput()
        id = graphene.String(required=True)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    experience = graphene.Field(ExperienceNode)

    @staticmethod
    def mutate(self, info, id=None, **args):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ["unauthenticated"]
            return UpdateExperience(success=False, errors=errors)
        else:
            experience = get_instance(Experience, id)
            experience.title = args.get('input').get('title', None)
            experience.name_of_company = args.get('input').get('name_of_company', None)
            experience.location = args.get('input').get('location', None)
            experience.start_date = args.get('input').get('start_date', None)
            experience.end_date = args.get('input').get('end_date', None)
            experience.save()
            return UpdateExperience(experience=experience, success=True, errors=None)


class CreateSkill(graphene.Mutation):
    class Arguments:
        input = SkillInput(description="These fields are required", required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    skill = graphene.Field(SkillNode)

    @staticmethod
    def mutate(self, info, **args):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ['unauthenticated']
            return CreateSkill(success=False, errors=errors)
        else:
            profile = Profile.objects.get(user=info.context.user)
            skill = Skill.objects.create(
                 profile=profile,
                 title=args.get('input').get('title', None),
                 )
            return CreateSkill(skill=skill, success=True, errors=None)


class UpdateSkill(graphene.Mutation):
    class Arguments:
        input = SkillInput()
        id = graphene.String(required=True)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    skill = graphene.Field(SkillNode)

    @staticmethod
    def mutate(self, info, id=None, **args):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ["unauthenticated"]
            return UpdateSkill(success=False, errors=errors)
        else:
            skill = get_instance(Skill, id)
            skill.title = args.get('input').get('title', None)
            skill.save()
            return UpdateSkill(skill=skill, success=True, errors=None)


class CreateLanguage(graphene.Mutation):
    class Arguments:
        input = LanguageInput(description="These fields are required", required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    language = graphene.Field(LanguageNode)

    @staticmethod
    def mutate(self, info, **args):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ['unauthenticated']
            return CreateLanguage(success=False, errors=errors)
        else:
            profile = Profile.objects.get(user=info.context.user)
            language = Language.objects.create(
                 profile=profile,
                 name=args.get('input').get('name', None),
                 )
            return CreateLanguage(language=language, success=True, errors=None)


class UpdateLanguage(graphene.Mutation):
    class Arguments:
        input = LanguageInput()
        id = graphene.String(required=True)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    language = graphene.Field(LanguageNode)

    @staticmethod
    def mutate(self, info, id=None, **args):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ["unauthenticated"]
            return UpdateLanguage(success=False, errors=errors)
        else:
            language = get_instance(Language, id)
            language.name = args.get('input').get('name', None)
            language.save()
            return UpdateLanguage(language=language, success=True, errors=None)


class CreateEducation(graphene.Mutation):
    class Arguments:
        input = EducationInput(description="These fields are required", required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    education = graphene.Field(EducationNode)

    @staticmethod
    def mutate(self, info, **args):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ['unauthenticated']
            return CreateEducation(success=False, errors=errors)
        else:
            profile = Profile.objects.get(user=info.context.user)
            education = Education.objects.create(
                 profile=profile,
                 title=args.get('input').get('title', None),
                 sub_title=args.get('input').get('sub_title', None),
                 start_date=args.get('input').get('start_date', None),
                 end_date=args.get('input').get('end_date', None),
                 )
            return CreateEducation(education=education, success=True, errors=None)


class UpdateEducation(graphene.Mutation):
    class Arguments:
        input = EducationInput()
        id = graphene.String(required=True)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    education = graphene.Field(EducationNode)

    @staticmethod
    def mutate(self, info, id=None, **args):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ["unauthenticated"]
            return UpdateEducation(success=False, errors=errors)
        else:
            education = get_instance(Education, id)
            education.title = args.get('input').get('title', None)
            education.sub_title = args.get('input').get('sub_title', None)
            education.start_date = args.get('input').get('start_date', None)
            education.end_date = args.get('input').get('end_date', None)
            education.save()
            return UpdateEducation(education=education, success=True, errors=None)


class CreateAchievement(graphene.Mutation):
    class Arguments:
        input = AchievementInput(description="These fields are required", required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    achievement = graphene.Field(AchievementNode)

    @staticmethod
    def mutate(self, info, **args):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ['unauthenticated']
            return CreateAchievement(success=False, errors=errors)
        else:
            profile = Profile.objects.get(user=info.context.user)
            print ("profile", profile, args)
            achievement = Achievement.objects.create(
                 profile=profile,
                 category=args.get('input').get('category', None),
                 title=args.get('input').get('title', None),
                 sub_title=args.get('input').get('sub_title', None),
                 description=args.get('input').get('description', None),
                 )
            return CreateAchievement(achievement=achievement, success=True, errors=None)


class UpdateAchievement(graphene.Mutation):
    class Arguments:
        input = AchievementInput()
        id = graphene.String(required=True)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    achievement = graphene.Field(AchievementNode)

    @staticmethod
    def mutate(self, info, id=None, **args):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ["unauthenticated"]
            return UpdateAchievement(success=False, errors=errors)
        else:
            # profile = Profile.objects.get(user=info.context.user)
            achievement = get_instance(Achievement, id)
            # achievement = Achievement.objects.get(profile=profile, id=args.get('input').get('id'))
            print ('achievement', achievement)
            achievement.category = args.get('input').get('category', None)
            achievement.title = args.get('input').get('title', None)
            achievement.sub_title = args.get('input').get('sub_title', None)
            achievement.description = args.get('input').get('description', None)
            achievement.save()
            return UpdateAchievement(achievement=achievement, success=True, errors=None)
