from graphene import relay, ObjectType, Field
from graphene_django.types import DjangoObjectType
from graphene_django.fields import DjangoConnectionField
from graphene_django.filter.fields import DjangoFilterConnectionField

from .models import (User as UserModel,
                     Profile,
                     Experience,
                     Skill,
                     Language,
                     Education,
                     Achievement
                     )


class User(DjangoObjectType):
    """
    User Node
    """
    class Meta:
        model = UserModel
        filter_fields = {
            'email': ['exact', ]
        }
        exclude_fields = ('password', 'is_superuser', )
        interfaces = (relay.Node, )


class ProfileNode(DjangoObjectType):
    class Meta:
        model = Profile
        interfaces = (relay.Node, )


class ExperienceNode(DjangoObjectType):
    class Meta:
        model = Experience
        interfaces = (relay.Node, )


class SkillNode(DjangoObjectType):
    class Meta:
        model = Skill
        interfaces = (relay.Node, )


class LanguageNode(DjangoObjectType):
    class Meta:
        model = Language
        interfaces = (relay.Node, )


class EducationNode(DjangoObjectType):
    class Meta:
        model = Education
        interfaces = (relay.Node, )


class AchievementNode(DjangoObjectType):
    class Meta:
        model = Achievement
        interfaces = (relay.Node, )


class UserQuery(object):
    """
    what is an abstract type?
    http://docs.graphene-python.org/en/latest/types/abstracttypes/
    """
    user = relay.Node.Field(User)
    users = DjangoFilterConnectionField(User)


class ProfileQuery(ObjectType):
    profile = Field(ProfileNode)
    profiles = DjangoConnectionField(ProfileNode)
    experience = Field(ExperienceNode)
    experiences = DjangoConnectionField(ExperienceNode)
    skill = Field(SkillNode)
    skills = DjangoConnectionField(SkillNode)
    language = Field(LanguageNode)
    languages = DjangoConnectionField(LanguageNode)
    education = Field(EducationNode)
    educations = DjangoConnectionField(EducationNode)
    achievement = Field(AchievementNode)
    achievements = DjangoConnectionField(AchievementNode)

    @staticmethod
    def resolve_profile(self, info, **kwargs):
        # print('info', info.context.user)
        if info.context.user.is_authenticated:
            return Profile.objects.get(user=info.context.user)
        return None


class Viewer(ObjectType):
    user = Field(User)

    def resolve_user(self, info, **kwargs):
        if info.context.user.is_authenticated:
            return info.context.user
        return None
