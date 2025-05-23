from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, JobOffer, Application, Message, Resource, Review, Comment
from .forms import JobOfferForm, ApplicationForm, MessageForm, ResourceForm, ReviewForm, CommentForm
from django.contrib.auth import authenticate, login
# from .forms import LoginForm, FreelancerRegistrationForm, ClientRegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import LoginForm, RegistrationForm
from .models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)  # Déconnecte l'utilisateur
    return redirect('login')  # Redirige vers la page de connexion


# Dashboard principal
# @login_required
def dashboard(request):
    return render(request, 'dashboard.html')

# Job Offers
# @login_required
def job_list(request):
    jobs = JobOffer.objects.all()
    return render(request, 'job/job_list.html', {'jobs': jobs})

# @login_required
def job_create(request):
    if request.method == 'POST':
        form = JobOfferForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.client = request.user.clientprofile
            job.save()
            return redirect('job_list')
    else:
        form = JobOfferForm()
    return render(request, 'job/job_form.html', {'form': form})

# @login_required
def job_update(request, pk):
    job = get_object_or_404(JobOffer, pk=pk)
    form = JobOfferForm(request.POST or None, instance=job)
    if form.is_valid():
        form.save()
        return redirect('job_list')
    return render(request, 'job/job_form.html', {'form': form})

# @login_required
def job_delete(request, pk):
    job = get_object_or_404(JobOffer, pk=pk)
    if request.method == 'POST':
        job.delete()
        return redirect('job_list')
    return render(request, 'job/job_confirm_delete.html', {'job': job})

# Application
# @login_required
def apply_to_job(request, job_id):
    job = get_object_or_404(JobOffer, id=job_id)
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.job = job
            app.freelancer = request.user.freelancerprofile
            app.save()
            messages.success(request, "Application sent.")
            return redirect('job_list')
    else:
        form = ApplicationForm()
    return render(request, 'job/application_form.html', {'form': form, 'job': job})

# Messaging
# @login_required
def inbox(request):
    messages_received = Message.objects.filter(receiver=request.user)
    return render(request, 'message/inbox.html', {'messages': messages_received})

# @login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.save()
            return redirect('inbox')
    else:
        form = MessageForm()
    return render(request, 'message/send_message.html', {'form': form})

# Resources
# @login_required
def resource_list(request):
    resources = Resource.objects.all()
    return render(request, 'resource/resource_list.html', {'resources': resources})

# @login_required
def resource_create(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.author = request.user
            resource.save()
            return redirect('resource_list')
    else:
        form = ResourceForm()
    return render(request, 'resource/resource_form.html', {'form': form})

# Review
# @login_required
def submit_review(request, user_id):
    reviewed_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.reviewed = reviewed_user
            review.save()
            return redirect('dashboard')
    else:
        form = ReviewForm()
    return render(request, 'review/review_form.html', {'form': form, 'user': reviewed_user})

# Comment
# @login_required
def comment_create(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.resource = resource
            comment.save()
            return redirect('resource_list')
    else:
        form = CommentForm()
    return render(request, 'comment/comment_form.html', {'form': form})
