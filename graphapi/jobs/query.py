from graphene import relay, ObjectType, Field
from graphene_django.types import DjangoObjectType
from graphene_django.fields import DjangoConnectionField
from graphene_django.filter.fields import DjangoFilterConnectionField

from apps.account.models import Company
from apps.job import models


class JobNode(DjangoObjectType):
    class Meta:
        model = models.Job
        interfaces = (relay.Node, )


class ResponsibilityNode(DjangoObjectType):
    class Meta:
        model = models.Responsibility
        interfaces = (relay.Node, )


class QualificationNode(DjangoObjectType):
    class Meta:
        model = models.Qualification
        interfaces = (relay.Node, )


class BenefitNode(DjangoObjectType):
    class Meta:
        model = models.Benefit
        interfaces = (relay.Node, )


class RoleNode(DjangoObjectType):
    class Meta:
        model = models.Role
        interfaces = (relay.Node, )


class CriteriaNode(DjangoObjectType):
    class Meta:
        model = models.Criteria
        interfaces = (relay.Node, )


class JobTypeNode(DjangoObjectType):
    class Meta:
        model = models.JobType
        interfaces = (relay.Node, )


class WorkingStructureNode(DjangoObjectType):
    class Meta:
        model = models.WorkingStructure
        interfaces = (relay.Node, )


class JobQuery(ObjectType):
    job = Field(JobNode)
    jobs = DjangoConnectionField(JobNode)
    responsibility = Field(ResponsibilityNode)
    responsibilities = DjangoConnectionField(ResponsibilityNode)
    qualification = Field(QualificationNode)
    qualifications = DjangoConnectionField(QualificationNode)
    benefit = Field(BenefitNode)
    benefits = DjangoConnectionField(BenefitNode)
    role = Field(RoleNode)
    roles = DjangoConnectionField(RoleNode)
    criteria = Field(CriteriaNode)
    criterias = DjangoConnectionField(CriteriaNode)
    working_structure = Field(WorkingStructureNode)
    working_structures = DjangoConnectionField(WorkingStructureNode)
    job_type = Field(JobTypeNode)
    job_types = DjangoConnectionField(JobTypeNode)
