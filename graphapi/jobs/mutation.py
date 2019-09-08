import graphene

from core.utils import get_instance
from apps.jobs.models import (Job, Responsibility, Qualification,
                     Benefit, WorkingStructure, Criteria, JobType,
                     Role)

from .input import (JobInput, ResponsibilityInput, QualificationInput, BenefitsInput,
                    WorkingStructureInput, CriteriaInput, JobTypeInput, RoleInput)


class CreateJob(graphene.Mutation):
    class Arguments:
        input = JobInput(description="These fields are required", required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    Job = graphene.Field(JobNode)

    @staticmethod
    def mutate(self, info, **args):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ['unauthenticated']
            return CreateJob(success=False, errors=errors)
        else:
            try:
                input_value = args.get('input')
                company_instance = Company.objects.get(id=input_value.get('id', None))
                Job = Job.objects.create(
                 company=company_instance,
                 title=input_value.get('title', None),
                 description=input_value.get('description', None),
                 minimum_experience=input_value.get('minimum_experience', None),
                 minimum_salary=input_value.get('minimum_salary', None),
                 deadline=input_value.get('deadline', None),
                 address=input_value.get('address', None),
                 city=input_value.get('city', None),
                 country=input_value.get('country', None),
                 state=input_value.get('state', None),
                 zip_code=input_value.get('zip_code', None),
                 branch=input_value.get('branch', None),
                 is_active=input_value.get('is_active', None),
            except Company.DoesNotExist:
                errors = ['No such company']
            return CreateJob(profile=profile, success=True, errors=None)


class UpdateJob(graphene.Mutation):
    class Arguments:
        input = JobInput(description="These fields are required", required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    job = graphene.Field(JobNode)

    @staticmethod
    def mutate(self, info, **args):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ['unauthenticated']
            return Updatejob(success=False, errors=errors)
        else:
            try:
                input_value = args.get('input')
                job = job.objects.get(company=input_value.get('id', None))
                job.title=input_value.get('title', None),
                job.description=input_value.get('description', None),
                job.minimum_experience=input_value.get('minimum_experience', None),
                job.minimum_salary=input_value.get('minimum_salary', None),
                job.deadline=input_value.get('deadline', None),
                job.address=input_value.get('address', None),
                job.city=input_value.get('city', None),
                job.country=input_value.get('country', None),
                job.state=input_value.get('state', None),
                job.zip_code=input_value.get('zip_code', None),
                job.branch=input_value.get('branch', None),
                job.is_active=input_value.get('is_active', None),
                job.save()
            except Job.DoesNotExist:
                errors = ["No such Job"]
            return UpdateJob(job=job, success=True, errors=None)


class CreateBenefits(graphene.Mutation):
    class Arguments:
        input = BenefitsInput(description="These fields are required", required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    benefits = graphene.Field(BenefitsNode)

    @staticmethod
    def mutate(self, info, id=None, **args):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ['unauthenticated']
            return CreateBenefits(success=False, errors=errors)
        else:
            input_value = args.get('input')
            company_instance = get_instance(Company, id)
            job = Job.objects.get(company=company_instance)
            responsibility = Benefits.objects.create(
                 job=job,
                 title=input_value.get('title', None),
                 )
            return CreateBenefits(benefits=benefits, success=True, errors=None)


class UpdateBenefits(graphene.Mutation):
    class Arguments:
        input = BenefitsInput()
        id = graphene.String(required=True)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    benefit = graphene.Field(BenefitsNode)

    @staticmethod
    def mutate(self, info, id=None, **args):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ["unauthenticated"]
            return UpdateBenefits(success=False, errors=errors)
        else:
            benefit = get_instance(Benefit, id)
            benefit.title = args.get('input').get('title', None)
            benefit.save()
            return UpdateBenefits(benefit=benefit, success=True, errors=None)


class CreateQualification(graphene.Mutation):
    class Arguments:
        input = QualificationInput(description="These fields are required", required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    qualification = graphene.Field(QualificationNode)

    @staticmethod
    def mutate(self, info, id=None, **args):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ['unauthenticated']
            return CreateResponsibility(success=False, errors=errors)
        else:
            input_value = args.get('input')
            company_instance = get_instance(Company, id)
            job = Job.objects.get(company=company_instance)
            qualification = Qualification.objects.create(
                 job=job,
                 title=input_value.get('title', None),
                 )
            return CreateQualification(qualification=qualification, success=True, errors=None)


class UpdateQualification(graphene.Mutation):
    class Arguments:
        input = QualificationInput()
        id = graphene.String(required=True)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    qualification = graphene.Field(QualificationNode)

    @staticmethod
    def mutate(self, info, id=None, **args):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ["unauthenticated"]
            return UpdateQualification(success=False, errors=errors)
        else:
            qualification = get_instance(Qualification, id)
            qualification.title = args.get('input').get('title', None)
            qualification.save()
            return UpdateQualification(qualification=qualification, success=True, errors=None)


class CreateCriteria(graphene.Mutation):
    class Arguments:
        input = CriteriaInput(description="These fields are required", required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    criteria = graphene.Field(CriteriaNode)

    @staticmethod
    def mutate(self, info, id=None, **args):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ['unauthenticated']
            return CreateCriteria(success=False, errors=errors)
        else:
            input_value = args.get('input')
            company_instance = get_instance(Company, id)
            job = Job.objects.get(company=company_instance)
            criteria = Criteria.objects.create(
                 job=job,
                 title=input_value.get('title', None),
                 )
            return CreateQualification(criteria=criteria, success=True, errors=None)


class UpdateCriteria(graphene.Mutation):
    class Arguments:
        input = CriteriaInput()
        id = graphene.String(required=True)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    criteria = graphene.Field(CriteriaNode)

    @staticmethod
    def mutate(self, info, id=None, **args):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ["unauthenticated"]
            return UpdateQualification(success=False, errors=errors)
        else:
            criteria = get_instance(Criteria, id)
            criteria.title = args.get('input').get('title', None)
            criteria.save()
            return UpdateQualification(criteria=criteria, success=True, errors=None)


class CreateQualification(graphene.Mutation):
    class Arguments:
        input = QualificationInput(description="These fields are required", required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    qualification = graphene.Field(QualificationNode)

    @staticmethod
    def mutate(self, info, id=None, **args):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ['unauthenticated']
            return CreateResponsibility(success=False, errors=errors)
        else:
            input_value = args.get('input')
            company_instance = get_instance(Company, id)
            job = Job.objects.get(company=company_instance)
            qualification = Qualification.objects.create(
                 job=job,
                 title=input_value.get('title', None),
                 )
            return CreateQualification(qualification=qualification, success=True, errors=None)


class UpdateQualification(graphene.Mutation):
    class Arguments:
        input = QualificationInput()
        id = graphene.String(required=True)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    qualification = graphene.Field(QualificationNode)

    @staticmethod
    def mutate(self, info, id=None, **args):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ["unauthenticated"]
            return UpdateQualification(success=False, errors=errors)
        else:
            qualification = get_instance(Qualification, id)
            qualification.title = args.get('input').get('title', None)
            qualification.save()
            return UpdateQualification(qualification=qualification, success=True, errors=None)

class CreateJobType(graphene.Mutation):
    class Arguments:
        input = JobTypeInput(description="These fields are required", required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    job_type = graphene.Field(JobTypeNode)

    @staticmethod
    def mutate(self, info, id=None, **args):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ['unauthenticated']
            return CreateJobType(success=False, errors=errors)
        else:
            input_value = args.get('input')
            company_instance = get_instance(Company, id)
            job = Job.objects.get(company=company_instance)
            job_type = JobType.objects.create(
                 job=job,
                 title=input_value.get('title', None),
                 )
            return CreateJobType(job_type=job_type, success=True, errors=None)


class UpdateJobType(graphene.Mutation):
    class Arguments:
        input = JobTypeInput()
        id = graphene.String(required=True)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    job_type = graphene.Field(JobTypeNode)

    @staticmethod
    def mutate(self, info, id=None, **args):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ["unauthenticated"]
            return UpdateJobType(success=False, errors=errors)
        else:
            job_type = get_instance(JobType, id)
            job_type.title = args.get('input').get('title', None)
            job_type.save()
            return UpdateJobType(job_type=job_type, success=True, errors=None)

class CreateRole(graphene.Mutation):
    class Arguments:
        input = RoleInput(description="These fields are required", required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    role = graphene.Field(RoleNode)

    @staticmethod
    def mutate(self, info, id=None, **args):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ['unauthenticated']
            return CreateRole(success=False, errors=errors)
        else:
            input_value = args.get('input')
            company_instance = get_instance(Company, id)
            job = Job.objects.get(company=company_instance)
            role = Role.objects.create(
                 job=job,
                 title=input_value.get('title', None),
                 )
            return CreateRole(role=role, success=True, errors=None)


class UpdateRole(graphene.Mutation):
    class Arguments:
        input = RoleInput()
        id = graphene.String(required=True)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    role = graphene.Field(RoleNode)

    @staticmethod
    def mutate(self, info, id=None, **args):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ["unauthenticated"]
            return UpdateRole(success=False, errors=errors)
        else:
            role = get_instance(Role, id)
            role.title = args.get('input').get('title', None)
            role.save()
            return UpdateRole(role=role, success=True, errors=None)


class CreateWorkingStructure(graphene.Mutation):
    class Arguments:
        input = WorkingStructureInput(description="These fields are required", required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    working_structure = graphene.Field(WorkingStructureNode)

    @staticmethod
    def mutate(self, info, id=None, **args):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ['unauthenticated']
            return CreateWorkingStructure(success=False, errors=errors)
        else:
            input_value = args.get('input')
            company_instance = get_instance(Company, id)
            job = Job.objects.get(company=company_instance)
            working_structure = WorkingStructure.objects.create(
                 job=job,
                 title=input_value.get('title', None),
                 )
            return CreateWorkingStructure(working_structure=working_structure, success=True, errors=None)


class UpdateWorkingStructure(graphene.Mutation):
    class Arguments:
        input = WorkingStructureInput()
        id = graphene.String(required=True)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    working_structure = graphene.Field(WorkingStructureNode)

    @staticmethod
    def mutate(self, info, id=None, **args):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ["unauthenticated"]
            return UpdateWorkingStructure(success=False, errors=errors)
        else:
            working_structure = get_instance(WorkingStructure, id)
            working_structure.title = args.get('input').get('title', None)
            working_structure.save()
            return UpdateWorkingStructure(working_structure=working_structure, success=True, errors=None)

