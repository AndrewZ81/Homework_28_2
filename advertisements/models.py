from django.db.models import Model, CharField


class Category(Model):

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    name = CharField(max_length=200, unique=True)
