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
    CreateProfile,
    UpdateProfile,
    CreateExperience,
    UpdateExperience,
    CreateSkill,
    UpdateSkill,
    CreateLanguage,
    UpdateLanguage,
    CreateEducation,
    UpdateEducation,
    CreateAchievement,
    UpdateAchievement,
    CreatePortfolio,
    UpdatePortfolio,
    CreatePortfolioGallery,
    UpdatePortfolioGallery,
    CreateCompany,
    UpdateCompany,
    CreateCompanyService,
    UpdateCompanyService,
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
    profile = CreateProfile.Field()
    updateProfile = UpdateProfile.Field()
    experience = CreateExperience.Field()
    updateExperience = UpdateExperience.Field()
    skill = CreateSkill.Field()
    updateSkill = UpdateSkill.Field()
    language = CreateLanguage.Field()
    updateLanguage = UpdateLanguage.Field()
    education = CreateEducation.Field()
    updateEducation = UpdateEducation.Field()
    achievement = CreateAchievement.Field()
    updateAchievement = UpdateAchievement.Field()
    portfolio = CreatePortfolio.Field()
    updatePortfolio = UpdatePortfolio.Field()
    portfolioGallery = CreatePortfolioGallery.Field()
    updatePortfolioGallery = UpdatePortfolioGallery.Field()
    company = CreateCompany.Field()
    updateCompany = UpdateCompany.Field()
    companyService = CreateCompanyService.Field()
    updateCompanyService = UpdateCompanyService.Field()


schema = graphene.Schema(query=RootQuery, mutation=Mutation)
