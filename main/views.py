from unicodedata import category
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import Tutorial, TutorialCategory, TutorialSeries
from .forms import NewUserForm

LOGIN_SUCCESSFUL = 'You are now logged in as %s'
SERIES_EMPTY = "Series '%s' is empty, it does not have any tutorials"
ELEMENT_NOT_FOUND = "'%s' was not found"

def single_slug(request, single_slug):
    categories = [c.slug for c in TutorialCategory.objects.all()]
    if single_slug in categories:
        matching_series = TutorialSeries.objects.filter(category__slug=single_slug)
        series_urls = {}
        for m in matching_series.all():
            try:
                part_one = Tutorial.objects.filter(series__series=m.series).earliest('published')
                series_urls[m] = part_one.slug
            except ObjectDoesNotExist:
                # Series does not have any tutorial so the user is redirected 
                # to the same page using the same 'single_slug' that was sent 
                # when the series is clicked on
                messages.warning(request, SERIES_EMPTY %(m.series))
                series_urls[m] = single_slug

        return render(request,
            'main/category.html',
            {'part_ones': series_urls}
        )
    
    tutorial = Tutorial.objects.get(slug = single_slug)
    if tutorial is not None:
        tutorialFromSeries = Tutorial.objects.filter(series__series=tutorial.series.series).order_by('published')
        tutorialIdx = list(tutorialFromSeries).index(tutorial)
        return render(request,
            'main/tutorial.html',
            {
                'tutorial': tutorial,
                'sidebar': tutorialFromSeries,
                'tutorialIdx': tutorialIdx
            }
        )

    messages.error(request, ELEMENT_NOT_FOUND %(single_slug))        
    return HttpResponse(f'{single_slug} does not correspond to anything')

# Create your views here.
def homepage(request):
    return render(request,
        template_name='main/categories.html',
        context={'categories': TutorialCategory.objects.all()})

def register(request):
    if request.method == 'POST':
        form = NewUserForm(data = request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'New account created: {username}')
            login(request, user)
            messages.info(request, LOGIN_SUCCESSFUL %(username))
            return redirect('main:homepage')
        else:
            for msg in form.error_messages:
                messages.error(request, f'{msg}: {form.error_messages[msg]}')

    form = NewUserForm()
    return render(request,
        'main/register.html',
        context={'form': form}
    )

def logout_request(request):
    logout(request)
    messages.info(request, 'Logged out successfully')
    return redirect('main:homepage')

def login_request(request):
    INVALID_USERNAME_OR_PASSWORD = 'Invalid username or password'
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, LOGIN_SUCCESSFUL %(username))
                return redirect('main:homepage')
            else:
                messages.error(request, INVALID_USERNAME_OR_PASSWORD)
        else:
                messages.error(request, INVALID_USERNAME_OR_PASSWORD)

    form = AuthenticationForm()
    return render(request,
        'main/login.html',
        {'form': form}
    )