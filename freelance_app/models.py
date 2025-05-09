from django.db import models
from django.contrib.auth.models import AbstractUser

# 🔹 Custom User model
class User(AbstractUser):
    is_freelancer = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)

# 🔹 Freelancer Profile
class FreelancerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.TextField()
    experience = models.TextField()
    portfolio_url = models.URLField(blank=True, null=True)
    cv_file = models.FileField(upload_to='cvs/', blank=True, null=True)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username

# 🔹 Client Profile
class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    description = models.TextField()
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.company_name

# 🔹 Job Offer
class JobOffer(models.Model):
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    is_remote = models.BooleanField(default=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField()

    def __str__(self):
        return self.title

# 🔹 Application
class Application(models.Model):
    job = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE)
    cover_letter = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('envoye', 'Envoyé'),
        ('accepte', 'Accepté'),
        ('rejete', 'Rejeté')
    ], default='envoye')
    applied_at = models.DateTimeField(auto_now_add=True)

# 🔹 Message
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

# 🔹 Resource
class Resource(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    file = models.FileField(upload_to='resources/', blank=True, null=True)
    published_at = models.DateTimeField(auto_now_add=True)

# 🔹 Review
class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    reviewed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
