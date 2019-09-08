from django.db import models
# from django.urls import reverse
from django.conf import settings
from django.dispatch import receiver
from djmoney.models.fields import MoneyField
from django.db.models.signals import post_save, post_delete, pre_save

from mptt.models import MPTTModel, TreeForeignKey

from . import validators
from core.utils import token_generator, create_slug

'''
    Project Basis and Per hour Basis
    Category can be
         Graphics & Design, Marketing, Accounting, Writing
         Video, Animation, Music, Programming, Business, Tutor, Cooking, Tution
         Interior Design.
'''


class Category(MPTTModel):
    token = models.CharField(default=token_generator, max_length=20, unique=True, editable=False)
    name = models.CharField(max_length=120, db_index=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField(max_length=120, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        ordering = ('name', )
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_slug_list(self):
        try:
            ancestors = self.get_ancestors(include_self=True)
        except:
            ancestors = []
        else:
            ancestors = [i.slug for i in ancestors]
        slugs = []
        for i in range(len(ancestors)):
            slugs.append('/'.join(ancestors[:i+1]))
        return slugs

    def __str__(self):
        return self.name


class WorkingProcess(models.Model):
    work_basis = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Working Process"
        verbose_name_plural = "Working Processes"

    def __str__(self):
        return self.work_basis


class Service(models.Model):
    token = models.CharField(default=token_generator, max_length=20, unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=100, blank=False, null=False, db_index=True)
    slug = models.SlugField(max_length=150, db_index=True)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    category = models.ManyToManyField(Category, related_name='categories', blank=True)
    description = models.TextField(blank=False, null=False, max_length=500)
    average_rating = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=4)
    purchases = models.PositiveIntegerField(default=0)
    work_process = models.ManyToManyField(WorkingProcess, related_name="work_process", blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # objects = ServiceManager()

    def get_avg_rating(self):
        if self.reviews.count():
            total = 0
            count = 0
            for review in self.reviews.all():
                total += review.rate
                count += 1
            avg = total / count
            return round(avg, 2)
        return 0

    def get_purchases(self):
        total = 0
        for entry in self.service_entries.filter(is_ordered=True):
            total += entry.quantity
        return total

    class Meta:
        index_together = (('id', 'slug'),)
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('services:service-detail', kwargs={'pk': self.pk})


class Picture(models.Model):
    token = models.CharField(default=token_generator, max_length=20, unique=True, editable=False)
    photo = models.ImageField(upload_to='pictures')
    description = models.TextField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ServicePicture(Picture):
    service = models.ForeignKey(Service, null=False, on_delete=models.CASCADE,
                                blank=False, related_name='service_photos')

    class Meta:
        verbose_name = "Service Picture"
        verbose_name_plural = "Service Pictures"


class Review(models.Model):
    token = models.CharField(default=token_generator, max_length=20, unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviewer')
    description = models.TextField(blank=True, max_length=300)
    rate = models.IntegerField(validators=[validators.validate_rate])
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reviews')

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        return self.user.username + ' - ' + str(self.rate)


class Favorite(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    ip = models.CharField(max_length=19)
    user_agent = models.TextField(blank=True, null=True)
    mark_favorite = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('service', 'ip',)

    @classmethod
    def create_favorite_for_count(cls, request, service):
        ip = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = request.META.get('REMOTE_ADDR') if ip is None else ip
        user_agent = request.META.get('HTTP_USER_AGENT')
        mark_favorite, created = cls.objects.get_or_create(service=service, ip=ip, user_agent=user_agent)
        return mark_favorite


@receiver(post_save, sender=Review)
def update_avg_rating_add_or_update(sender, instance, **kwargs):
    service = instance.service
    service.average_rating = service.get_avg_rating()
    service.save()


@receiver(post_delete, sender=Review)
def update_avg_rating_delete(sender, instance, **kwargs):
    service = instance.service
    service.average_rating = service.get_avg_rating()
    service.save()


@receiver(pre_save, sender=Service)
def create_slug_on_name_create_or_update(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(sender, instance)
