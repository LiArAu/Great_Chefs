from django.db import models
from django.contrib.auth.models import User, Group
import uuid
from django.utils.translation import gettext as _
from django_scopes import ScopedManager, scopes_disabled
from annoying.fields import AutoOneToOneField
# from django_prometheus.models import ExportModelOperationsMixin
from greatchefs.settings import (COMMENT_PREF_DEFAULT, FRACTION_PREF_DEFAULT, KJ_PREF_DEFAULT, STICKY_NAV_PREF_DEFAULT)


def default_valid_until():
    return date.today() + timedelta(days=14)

class Category(models.Model):
    category = models.CharField(max_length = 15)

    def __str__(self):
        return self.category

class ShareZone(models.Model):
    name = models.CharField(max_length=128, default='Default')
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=512, default='', blank=True)
    max_recipes = models.IntegerField(default=0)
    max_storage_mb = models.IntegerField(default=0, help_text=_('Maximum file storage for space in MB. 0 for unlimited, -1 to disable file upload.'))
    max_users = models.IntegerField(default=0)
    allow_sharing = models.BooleanField(default=True)
    demo = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class RecipeContent(models.Model):
    title = models.CharField(max_length = 100)
    abstract = models.CharField(max_length = 500)
    full_content = models.CharField(max_length = 5000, null = True, blank = True)
    working_time = models.IntegerField(default=0)
    category = models.ManyToManyField(Category)
    pub_time = models.DateTimeField(auto_now_add = True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    pictures = models.ImageField(null = True, blank = True, upload_to = 'recipe_images/')
    sharezone = models.ForeignKey(ShareZone, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Comment(models.Model):
    recipe = models.ForeignKey(RecipeContent, on_delete=models.CASCADE)
    text = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ScopedManager(sharezone='recipe__sharezone')

    @staticmethod
    def get_zone_key():
        return 'recipe', 'sharezone'

    def get_zone(self):
        return self.recipe.sharezone

    def __str__(self):
        return self.text

# class InviteLink(models.Model):
#     uuid = models.UUIDField(default=uuid.uuid4)
#     email = models.EmailField(blank=True)
#     group = models.ForeignKey(Group, on_delete=models.CASCADE)
#     valid_until = models.DateField(default=default_valid_until)
#     used_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='used_by')
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     sharezone = models.ForeignKey(ShareZone, on_delete=models.CASCADE)
#     objects = ScopedManager(sharezone='sharezone')
#
#     def __str__(self):
#         return f'{self.uuid}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    # category = models.ManyToManyField('Category')
    # comments = models.BooleanField(default=COMMENT_PREF_DEFAULT)
    created_at = models.DateTimeField(auto_now_add=True)
    sharezone = models.ForeignKey(ShareZone, on_delete=models.CASCADE, null=True)
    zone_created = models.BooleanField(default=False)
    objects = ScopedManager(sharezone='sharezone')
    # tell django what to print
    def __str__(self):
        return self.user.username

class SearchFields(models.Model):
    name = models.CharField(max_length=32, unique=True)
    field = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return _(self.name)

    @staticmethod
    def get_name(self):
        return _(self.name)


def allSearchFields():
    return list(SearchFields.objects.values_list('id', flat=True))

def nameSearchField():
    return [SearchFields.objects.get(name='Name').id]

class SearchPreference(models.Model):
    # Search Style (validation parsleyjs.org)
    # phrase or plain or raw (websearch and trigrams are mutually exclusive)
    SIMPLE = 'plain'
    PHRASE = 'phrase'
    WEB = 'websearch'
    RAW = 'raw'
    SEARCH_STYLE = (
        (SIMPLE, _('Simple')),
        (PHRASE, _('Phrase')),
        (WEB, _('Web')),
        (RAW, _('Raw'))
    )

    user = AutoOneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    search = models.CharField(choices=SEARCH_STYLE, max_length=32, default=SIMPLE)

    lookup = models.BooleanField(default=False)
    unaccent = models.ManyToManyField(SearchFields, related_name="unaccent_fields", blank=True, default=allSearchFields)
    icontains = models.ManyToManyField(SearchFields, related_name="icontains_fields", blank=True, default=nameSearchField)
    istartswith = models.ManyToManyField(SearchFields, related_name="istartswith_fields", blank=True)
    trigram = models.ManyToManyField(SearchFields, related_name="trigram_fields", blank=True, default=nameSearchField)
    fulltext = models.ManyToManyField(SearchFields, related_name="fulltext_fields", blank=True)
    trigram_threshold = models.DecimalField(default=0.1, decimal_places=2, max_digits=3)
