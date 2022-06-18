from PIL import Image
from django.db.models import Model,\
                            JSONField,\
                            FloatField,\
                            ImageField,\
                            DateTimeField,\
                            ForeignKey,\
                            SET_NULL,\
                            CharField


def upload_to(instance, filename):
    return f'products/{filename}'


class Category(Model):
    title = JSONField()
    parent = ForeignKey('self', SET_NULL, 'children', null=True, blank=True, default=None)

    def __str__(self):
        return self.title['uz']


class Product(Model):
    # image_height = CharField(max_length=10, null=True, blank=True, editable=False, default="300")
    # image_width = CharField(max_length=10, null=True, blank=True, editable=False, default="300")

    price = FloatField(default=0)
    title = JSONField()
    image = ImageField(upload_to=upload_to, null=True)
    desc = JSONField(null=True)

    category = ForeignKey(Category, SET_NULL, 'products', null=True)
    created_at = DateTimeField(auto_now_add=True)

    def save(self):
        if not self.image:
            return

        super().save()
        image = Image.open(self.image)
        (width, height) = image.size
        size = (300, 300)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.image.path)

    def __str__(self):
        return self.title['uz']


