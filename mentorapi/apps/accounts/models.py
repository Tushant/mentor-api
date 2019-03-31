# roles - freelancer, hirer, company
# level of seller and buyer
# ratings, bids, messages, job
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwars):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email, password=password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    USER_TYPE_CHOICES = (
      ('tyalent', 'tyalent'),
      ('trustee', 'trustee'),  # may be the name IMP justifies the name
      ('company', 'company'),
      )
    role = models.CharField(choices=USER_TYPE_CHOICES, max_length=20, default='tyalent')
    objects = UserManager()

    def __str__(self):
        return self.email


User._meta.get_field('email')._unique = True
User._meta.get_field('username')._unique = False


# may be use slug later
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=100, blank=True, null=True)
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    name_of_company = models.CharField(max_length=150, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.PositiveSmallIntegerField(blank=True, null=True)
    slogan = models.CharField(max_length=400, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return f"{self.user.email}"


class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="experience")
    title = models.CharField(max_length=150, blank=False, null=False)
    name_of_company = models.CharField(max_length=150, blank=False, null=False)
    location = models.CharField(max_length=150, blank=False, null=False)
    start_date = models.DateField(max_length=150, blank=False, null=False)
    end_date = models.DateField(max_length=150, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"

    def __str__(self):
        return self.title


class Skill(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="skill")
    title = models.CharField(max_length=150, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

    def __str__(self):
        return self.title


class Language(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="language")
    name = models.CharField(max_length=150, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"

    def __str__(self):
        return self.name


class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="education")
    title = models.CharField(max_length=150, blank=False, null=False)
    sub_title = models.CharField(max_length=150, blank=True, null=True)
    start_date = models.DateField(max_length=150, blank=False, null=False)
    end_date = models.DateField(max_length=150, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Education"
        verbose_name_plural = "Educations"

    def __str__(self):
        return self.title


class Achievement(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="achievement")
    category = models.CharField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=250, blank=False, null=False)
    sub_title = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Achievement"
        verbose_name_plural = "Achievements"

    def __str__(self):
        return f"{self.category} - {self.title}"


class Portfolio(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="portfolio")
    category = models.CharField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=250, blank=False, null=False)
    sub_title = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='portfolio/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Portfolio"
        verbose_name_plural = "Portfolios"

    def __str__(self):
        return f"{self.title}"


class Gallery(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="gallery")
    title = models.CharField(max_length=250, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='portfolio/gallery/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Gallery"
        verbose_name_plural = "Galleries"

    def __str__(self):
        return f"{self.portfolio.title} - {self.title}"


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="company")
    name_of_company = models.CharField(max_length=200, blank=False, null=False)
    pan_number = models.CharField(max_length=100, blank=False, null=False)
    phone = models.CharField(max_length=20, blank=False, null=False)
    mobile = models.CharField(max_length=20, blank=False, null=False)
    email = models.EmailField(max_length=20, blank=False, null=False)
    number_of_employees = models.PositiveSmallIntegerField(blank=False, null=False, default=1)
    # address
    city = models.CharField(max_length=100, blank=False, null=False)
    address = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=False, null=False)
    zip_code = models.PositiveSmallIntegerField(blank=True, null=True)
    # may be ask for timezone, currency

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return f"{self.company.name_of_company}"


class Service(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="services")
    title = models.CharField(max_length=250, blank=False, null=False)
    sub_title = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='company/services/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return f"{self.company.name_of_company} - {self.title}"

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     print("instance", instance)
#     instance.profile.save()
