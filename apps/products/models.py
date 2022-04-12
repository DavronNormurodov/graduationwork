from django.db.models import Model,\
                            JSONField,\
                            FloatField,\
                            ImageField,\
                            DateTimeField,\
                            ForeignKey,\
                            SET_NULL


def upload_to(instance, filename):
    return f'products/{filename}'


class Category(Model):
    title = JSONField()
    parent = ForeignKey('self', SET_NULL, 'children', null=True, blank=True, default=None)

    def __str__(self):
        return self.title['uz']


class Product(Model):
    price = FloatField(default=0)
    title = JSONField()
    image = ImageField(upload_to=upload_to, null=True)
    desc = JSONField(null=True)

    category = ForeignKey(Category, SET_NULL, 'products', null=True)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title['uz']


