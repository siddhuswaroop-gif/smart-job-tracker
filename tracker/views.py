from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from .models import JobApplication


def login_view(request):

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')

        return render(request, 'tracker/login.html', {
            'error': 'Invalid username or password'
        })

    return render(request, 'tracker/login.html')


def signup_view(request):

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'tracker/signup.html', {
                'error': 'Username already exists'
            })

        User.objects.create_user(username=username, password=password)

        return redirect('login')

    return render(request, 'tracker/signup.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def index(request):

    applications = JobApplication.objects.filter(user=request.user)

    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')

    if search_query:
        applications = applications.filter(
            company_name__icontains=search_query
        )

    if status_filter:
        applications = applications.filter(status=status_filter)

    applications = applications.order_by('-applied_date')

    stats = JobApplication.objects.filter(user=request.user) \
        .values('status') \
        .annotate(count=Count('status'))

    status_counts = {
        'APPLIED': 0,
        'INTERVIEW': 0,
        'REJECTED': 0,
        'OFFER': 0
    }

    for item in stats:
        status_counts[item['status']] = item['count']

    return render(request, 'tracker/index.html', {
        'applications': applications,
        'status_counts': status_counts,
        'search_query': search_query,
        'status_filter': status_filter
    })


@login_required
def add_application(request):

    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        job_role = request.POST.get('job_role')
        status = request.POST.get('status')
        notes = request.POST.get('notes')
        resume = request.FILES.get('resume')

        JobApplication.objects.create(
            user=request.user,
            company_name=company_name,
            job_role=job_role,
            status=status,
            notes=notes,
            resume=resume
        )

        return redirect('index')

    return render(request, 'tracker/add_application.html')


@login_required
def edit_application(request, id):

    application = get_object_or_404(
        JobApplication,
        id=id,
        user=request.user
    )

    if request.method == 'POST':
        application.company_name = request.POST.get('company_name')
        application.job_role = request.POST.get('job_role')
        application.status = request.POST.get('status')
        application.notes = request.POST.get('notes')

        resume = request.FILES.get('resume')
        if resume:
            application.resume = resume

        application.save()

        return redirect('index')

    return render(request, 'tracker/edit_application.html', {
        'app': application
    })


@login_required
def delete_application(request, id):

    application = get_object_or_404(
        JobApplication,
        id=id,
        user=request.user
    )

    application.delete()

    return redirect('index')
