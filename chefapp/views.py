from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User
from .models import *
from .forms import *
from django.db.models import Q
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from collections import OrderedDict
from django.utils.translation import gettext as _
from django_scopes import scopes_disabled
import uuid
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.exceptions import ValidationError


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account has been created for {username}!')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'chefapp/register.html', {'form': form})

@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipePublishForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            publisher = request.user
            messages.success(request, f'{publisher}, Thank you for sharing the recipe with us!')
            return redirect('home')
    else:
        form = RecipePublishForm()
    return render(request, 'chefapp/add.html', {'form':form})


@login_required
def zone(request):
    if request.user.userprofile.zone_created == True:
        zonename = request.user.userprofile.sharezone.name
        recipes = OrderedDict.fromkeys(RecipeContent.objects.filter(sharezone=request.user.userprofile.sharezone).all().order_by('title'))
        return render(request, 'chefapp/sharezone.html', {'zonename': zonename, 'recipelist':recipes})
    else:
        if request.method == 'POST':
            create_form = SharezoneCreationForm(request.POST,prefix='create')
            if create_form.is_valid():
                created_zone = ShareZone.objects.create(
                    name=create_form.cleaned_data['name'],
                    created_by=request.user,
                    max_storage_mb=settings.SHAREZONE_DEFAULT_MAX_FILES,
                    max_recipes=settings.SHAREZONE_DEFAULT_MAX_RECIPES,
                    max_users=settings.SHAREZONE_DEFAULT_MAX_USERS,
                    allow_sharing=settings.SHAREZONE_DEFAULT_ALLOW_SHARING,
                )

                request.user.userprofile.sharezone = created_zone
                request.user.userprofile.zone_created = True
                request.user.userprofile.save()

                messages.add_message(request, messages.SUCCESS,_('Your sharezone is ready. Start by adding some recipes or invite other people to join you.'))
                return redirect('home')
        else:
            create_form = SharezoneCreationForm()
        return render(request, 'chefapp/no_space_info.html', {'create_form': create_form})



@login_required
def home(request):
    recipes = OrderedDict.fromkeys(RecipeContent.objects.order_by('pub_time'))
    return render(request, 'chefapp/home.html', {'recipelist': recipes})

def no_perm(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, _('You are not logged in and therefore cannot view this page!'))
        return redirect('login')
    return render(request, 'chefapp/no_perm_info.html')

class RecipeDetailView(generic.DetailView):
    model = RecipeContent

class CatDetailView(generic.DetailView):
    model = Category
    def get_context(self, **kwargs):
        context = super(catDetailView,self).get_context_data(**kwargs)
        recipes = OrderedDict.fromkeys(RecipeContent.objects.filter(category = self.kwargs['pk']).order_by('-id'))
        context['recipelist'] = recipes
        return context

class ProfDetailView(generic.DetailView):
    model = UserProfile
