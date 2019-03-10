import graphene


class ProfileInput(graphene.InputObjectType):

    full_name = graphene.String(description='Full Name')
    age = graphene.String(description='Age')
    city = graphene.String(description='City')
    address = graphene.String(description='Address')
    name_of_company = graphene.String(description='Name of Company')
    job_title = graphene.String(description='Job Title')
    zip_code = graphene.String(description='Zip Code')
    slogan = graphene.String(description='Slogan')
    bio = graphene.String(description='Bio')
    website = graphene.String(description='Website')
    github = graphene.String(description='Github')
    twitter = graphene.String(description='Twitter')
    linkedin = graphene.String(description='Linked in')
    facebook = graphene.String(description='Facebook')


class ExperienceInput(graphene.InputObjectType):

    title = graphene.String(description='Title')
    name_of_company = graphene.String(description='Name of Company')
    location = graphene.String(description='Location')
    start_date = graphene.String(description='Start Date')
    end_date = graphene.String(description='End Date')


class SkillInput(graphene.InputObjectType):

    title = graphene.String(description='Title of Skill')


class LanguageInput(graphene.InputObjectType):

    name = graphene.String(description='Name of Language')


class EducationInput(graphene.InputObjectType):

    title = graphene.String(description='Title of Education')
    sub_title = graphene.String(description='Sub Title of Education')
    start_date = graphene.String(description='Start Date')
    end_date = graphene.String(description='End Date')


class AchievementInput(graphene.InputObjectType):

    category = graphene.String(description='Category')
    title = graphene.String(description='Title')
    sub_title = graphene.String(description='Sub Title')
    description = graphene.String(description='Description')
