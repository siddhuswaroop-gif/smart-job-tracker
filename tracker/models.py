from django.db import models
from django.contrib.auth.models import User


class JobApplication(models.Model):

    STATUS_CHOICES = [
        ('APPLIED', 'Applied'),
        ('INTERVIEW', 'Interview'),
        ('REJECTED', 'Rejected'),
        ('OFFER', 'Offer'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    company_name = models.CharField(max_length=200)
    job_role = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APPLIED')
    notes = models.TextField(blank=True, null=True)

    resume = models.FileField(upload_to='resumes/', blank=True, null=True)  # ⭐ NEW FIELD

    applied_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} - {self.job_role}"
