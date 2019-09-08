from django.db import models

from djmoney.models.fields import MoneyField

# maybe i need to use this category model in generic models section
from core.utils import token_generator
from apps.services.models import Category, WorkingProcess


class Requirement(models.Model):
    title = models.CharField(max_length=250, blank=False, null=False)
    description = models.TextField()

    class Meta:
        verbose_name = "Requirement"
        verbose_name_plural = "Requirements"

    def __str__(self):
        return self.title


class Project(models.Model):
    # need to associate user and bid
    token = models.CharField(default=token_generator, max_length=20, unique=True, editable=False)
    title = models.CharField(max_length=250, blank=False, null=False)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, null=False)
    work_process = models.ForeignKey(WorkingProcess, on_delete=models.CASCADE, blank=False, null=False)
    budget = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    preference = models.CharField(max_length=200)
    requirement = models.ForeignKey(Requirement, on_delete=models.CASCADE)
    # not sure how to present but for now adjusting with just a simple charfield
    # deadline can be in date or 2 weeks, 1 month time way
    deadline = models.CharField(max_length=100, blank=True, null=True)
    is_available = models.BooleanField(default=True, help_text="completed")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.token + self.title
