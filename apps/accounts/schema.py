from channels.layers import get_channel_layer
from graphene import relay, ObjectType, Field
from graphene_django.types import DjangoObjectType
from graphene_django.fields import DjangoConnectionField
from graphene_django.filter.fields import DjangoFilterConnectionField
from asgiref.sync import async_to_sync
from django.core import serializers

from . import models


class User(DjangoObjectType):
    """
    User Node
    """
    class Meta:
        model = models.User
        filter_fields = {
            'email': ['exact', ]
        }
        exclude_fields = ('password', 'is_superuser', )
        interfaces = (relay.Node, )


class ProfileNode(DjangoObjectType):
    class Meta:
        model = models.Profile
        interfaces = (relay.Node, )


class ExperienceNode(DjangoObjectType):
    class Meta:
        model = models.Experience
        interfaces = (relay.Node, )


class SkillNode(DjangoObjectType):
    class Meta:
        model = models.Skill
        interfaces = (relay.Node, )


class LanguageNode(DjangoObjectType):
    class Meta:
        model = models.Language
        interfaces = (relay.Node, )


class EducationNode(DjangoObjectType):
    class Meta:
        model = models.Education
        interfaces = (relay.Node, )


class AchievementNode(DjangoObjectType):
    class Meta:
        model = models.Achievement
        interfaces = (relay.Node, )


class PortfolioNode(DjangoObjectType):
    class Meta:
        model = models.Portfolio
        interfaces = (relay.Node, )


class PortfolioGalleryNode(DjangoObjectType):
    class Meta:
        model = models.Gallery
        interfaces = (relay.Node, )


class CompanyNode(DjangoObjectType):
    class Meta:
        model = models.Company
        interfaces = (relay.Node, )


class CompanyServiceNode(DjangoObjectType):
    class Meta:
        model = models.Service
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
    company = Field(CompanyNode)
    companies = DjangoConnectionField(CompanyNode)
    service = Field(CompanyServiceNode)
    services = DjangoConnectionField(CompanyServiceNode)
    portfolio = Field(PortfolioNode)
    portfolios = DjangoConnectionField(PortfolioNode)
    gallery = Field(PortfolioGalleryNode)
    galleries = DjangoConnectionField(PortfolioGalleryNode)

    @staticmethod
    def resolve_profile(self, info, **kwargs):
        if info.context.user.is_authenticated:
            channel_layer = get_channel_layer()
            percent = async_to_sync(channel_layer.send)('accounts', {
                'type': 'calculate.profile.percentage',
                'user': serializers.serialize('json', [info.context.user, ])
            })
            print("percent")
            print("is", percent)
            return models.Profile.objects.get(user=info.context.user)
        return None


class Viewer(ObjectType):
    user = Field(User)

    def resolve_user(self, info, **kwargs):
        if info.context.user.is_authenticated:
            return info.context.user
        return None
