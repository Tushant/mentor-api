import random
import string

from django.utils.text import slugify

from graphql_relay.node.node import from_global_id


def token_generator():
    return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(9))


def create_slug(model, instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = model.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def get_instance(_object, encoded_id, slug=False, otherwise=None):
    print("")
    try:
        if slug:
            return _object.objects.get(slug=encoded_id)
        else:
            return _object.objects.get(pk=from_global_id(encoded_id)[1])
    except _object.DoesNotExist:
        return otherwise
