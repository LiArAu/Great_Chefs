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
from chefapp.helper.permissions import group_required, has_group_permission

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account has been created for {username}!')
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'recipeapp/register.html', {'form': form})

@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipePublishForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            publisher = form.cleaned_data.get('publisher')
            messages.success(request, f'{publisher}, Thank you for sharing the recipe with us!')
            return redirect('home')
    else:
        form = RecipePublishForm()
    return render(request, 'chefapp/add.html', {'form':form})


@login_required
def nozone(request):
    if request.method == 'POST':
        create_form = SharezoneCreationForm(request.POST,prefix='create')
        join_form = SharezoneJoinForm(request.POST,prefix='join')
        if create_form.is_valid():
            created_zone = ShareZone.objects.create(
                name=create_form.cleaned_data['name'],
                created_by=request.user,
                max_file_storage_mb=settings.SHAREZONE_DEFAULT_MAX_FILES,
                max_recipes=settings.SHAREZONE_DEFAULT_MAX_RECIPES,
                max_users=settings.SHAREZONE_DEFAULT_MAX_USERS,
                allow_sharing=settings.SHAREZONE_DEFAULT_ALLOW_SHARING,
            )

            request.user.userpreference.sharezone = created_zone
            request.user.userpreference.save()
            request.user.groups.add(Group.objects.filter(name='admin').get())

            messages.add_message(request, messages.SUCCESS,_('Your sharezone is ready. Start by adding some recipes or invite other people to join you.'))
            return HttpResponseRedirect(reverse('index'))

        if join_form.is_valid():
            return HttpResponseRedirect(reverse('view_invite', args=[join_form.cleaned_data['token']]))
    else:
        create_form = SharezoneCreationForm()
        join_form = SharezoneJoinForm()
    return render(request, 'chefapp/nozone.html', {'create_form': create_form, 'join_form': join_form})

@group_required('admin')
def havezone(request):
    sharezone_users = UserPreference.objects.filter(sharezone=request.sharezone).all()
    counts = Object()
    counts.recipes = RecipeContent.objects.filter(sharezone=request.sharezone).count()
    counts.comments = Comment.objects.filter(recipe__sharezone=request.sharezone).count()

    invite_links = InviteLink.objects.filter(valid_until__gte=datetime.today(), used_by=None, sharezone=request.sharezone).all()
    RequestConfig(request, paginate={'per_page': 25}).configure(invite_links)

    return render(request, 'sharezone.html', {'sharezone_users': sharezone_users, 'counts': counts, 'invite_links': invite_links})


@login_required
def home(request):
    recipes = OrderedDict.fromkeys(RecipeContent.objects.filter(Q(category__in = request.user.userprofile.category.all())).order_by('-id'))
    return render(request, 'chefapp/home.html',{'recipelist': recipes})

class RecipeDetailView(generic.DetailView):
    model = RecipeContent

class CatDetailView(generic.DetailView):
    model = Category
    def get_context(self, **kwargs):
        context = super(catDetailView,self).get_context_data(**kwargs)
        recipes = OrderedDict.fromkeys(RecipeContent.objects.filter(category = self.kwargs['pk']).order_by('-id'))
        context['recipelist'] = recipes
        return context
