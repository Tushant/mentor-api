import graphene
import graphql_social_auth

from apps.accounts.schema import ProfileQuery
from apps.accounts.mutations import (
    Activate,
    DeleteAccount,
    Login,
    RefreshToken,
    Register,
    ResetPassword,
    ResetPasswordConfirm,
    ProfileMutation,
    ExperienceMutation,
    SkillMutation,
    LanguageMutation,
    EducationMutation,
    AchievementMutation
)

from apps.accounts.schema import Viewer


class RootQuery(ProfileQuery, graphene.ObjectType):
    viewer = graphene.Field(Viewer)

    def resolve_viewer(self, info, **kwargs):
        if info.context.user.is_authenticated:
            return info.context.user
        return None


class Mutation(graphene.ObjectType):
    activate = Activate.Field()
    login = Login.Field()
    register = Register.Field()
    deleteAccount = DeleteAccount.Field()
    refreshToken = RefreshToken.Field()
    resetPassword = ResetPassword.Field()
    resetPasswordConfirm = ResetPasswordConfirm.Field()
    social_auth = graphql_social_auth.SocialAuth.Field()
    profile = ProfileMutation.Field()
    experience = ExperienceMutation.Field()
    skill = SkillMutation.Field()
    language = LanguageMutation.Field()
    education = EducationMutation.Field()
    achievement = AchievementMutation.Field()


schema = graphene.Schema(query=RootQuery, mutation=Mutation)
