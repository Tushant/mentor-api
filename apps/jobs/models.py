import datetime
from django.db import models
from django.db.models.signals import post_save

from apps.accounts.models import Company
from core.utils import create_slug

# role, job_type, category, skills


class Job(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="job")
    title = models.CharField(max_length=250, blank=False, null=False)
    slug = models.SlugField()
    description = models.TextField(blank=False, null=False)
    minimum_experience = models.PositiveSmallIntegerField(
        blank=False, null=False)
    minimum_salary = models.PositiveSmallIntegerField(blank=False, null=False)
    deadline = models.DateField(default=datetime.date.today)
    city = models.CharField(max_length=100, blank=False, null=False)
    address = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=False, null=False)
    zip_code = models.PositiveSmallIntegerField(blank=True, null=True)
    branch = models.CharField(max_length=100, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'

    def __str__(self):
        return f'{self.title}'

    def save(self, **kwargs):
        slug = self.title
        create_slug(self, slug)
        super(Job, self).save()


class Responsibility(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE,
                            related_name="job_responsibility")
    title = models.TextField(blank=False, null=False)

    class Meta:

        verbose_name = 'Responsibility'
        verbose_name = 'Responsibilities'

    def __str__(self):
        return f"{self.job.__str__()} - {self.title}[:25]"


class Qualification(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE,
                            related_name="job_qualification")
    title = models.TextField(blank=False, null=False)

    class Meta:

        verbose_name = 'Qualification'
        verbose_name = 'Qualifications'

    def __str__(self):
        return f"{self.job.__str__()} - {self.title}[:25]"


class Benefit(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE,
                            related_name="job_benefit")
    title = models.TextField(blank=False, null=False)

    class Meta:

        verbose_name = 'Responsibility'
        verbose_name = 'Responsibilities'

    def __str__(self):
        return f"{self.job.__str__()} - {self.title}[:25]"


class WorkingStructure(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE,
                            related_name="job_working_structure")
    title = models.TextField(blank=False, null=False)

    class Meta:

        verbose_name = 'Working Structure'
        verbose_name = 'Working Structures'

    def __str__(self):
        return f"{self.job.__str__()} - {self.title}[:25]"


class Criteria(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE,
                            related_name="job_criteria")
    title = models.TextField(blank=False, null=False)

    class Meta:

        verbose_name = 'Criteria'
        verbose_name = 'Criterias'

    def __str__(self):
        return f"{self.job.__str__()} - {self.title}[:25]"


class JobType(models.Model):
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name="job_type")
    title = models.CharField(max_length=100, blank=False, null=False)

    class Meta:

        verbose_name = 'Job Type'
        verbose_name = 'Job Types'

    def __str__(self):
        return f"{self.job.__str__()} - {self.title}"


class Role(models.Model):
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name="job_role")
    title = models.CharField(max_length=150, blank=False, null=False)

    class Meta:

        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return f"{self.job.__str__()} -{self.title}"
