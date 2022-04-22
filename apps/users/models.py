from django.db.models import Model,\
                            JSONField,\
                            BooleanField,\
                            CharField

lang_choice = (
    ('uz', 'Uzbek'),
    ('ru', 'Russian')
)
status_choice = (
    ('active', 'Active'),
    ('cancelled', 'Cancelled'),
    ('delivered', 'Delivered')
)


class User(Model):
    chat_id = JSONField(max_length=50)
    name = JSONField(max_length=50, null=True)
    contact_number = JSONField(max_length=20, null=True)
    lang = JSONField(max_length=2, choices=lang_choice, null=True)
    verify = BooleanField(default=False)

    def __str__(self):
        return self.name


class Admins(Model):
    chat_id = CharField(max_length=50)
    name = CharField(max_length=50)
