import graphene


class JobInput(graphene.InputObjectType):

    company = graphene.String(description='Company')
    title = graphene.String(description='Job Title')
    description = graphene.String(description='Description')
    minimum_experience = graphene.String(description='Minimum Experience')
    minimum_salary = graphene.String(description='Minimum Salary')
    deadline = graphene.String(description='Deadline')
    address = graphene.String(description='Address')
    zip_code = graphene.String(description='Zip Code')
    city = graphene.String(description='City')
    state = graphene.String(description='State')
    country = graphene.String(description='Country')
    branch = graphene.String(description='Branch')
    is_active = graphene.String(description='Is it Active?')


class ResponsibilityInput(graphene.InputObjectType):

    title = graphene.String(description='Title')


class QualificationInput(graphene.InputObjectType):

    title = graphene.String(description='Title')


class BenefitsInput(graphene.InputObjectType):

    title = graphene.String(description='Title of Skill')


class WorkingStructureInput(graphene.InputObjectType):

    name = graphene.String(description='Name of Language')


class CriteriaInput(graphene.InputObjectType):

    title = graphene.String(description='Title of Education')


class JobTypeInput(graphene.InputObjectType):

    title = graphene.String(description='Title')


class RoleInput(graphene.InputObjectType):

    title = graphene.String(description='Title')
