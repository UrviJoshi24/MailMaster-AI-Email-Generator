from django.db import models
from django.contrib.auth.models import User

class SubjectLine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links to the user who generated the subject line
    content = models.TextField()  # Content entered by the user
    ai_generated = models.TextField()  # AI-generated subject line
    edited_subject = models.TextField(blank=True, null=True)  # User-edited subject line
    save_as = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of when it was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp of when it was last edited

    def __str__(self):
        return f"Subject Line by {self.user.username} on {self.created_at}"

class EmailReply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links to the user who generated the reply
    email_body = models.TextField()  # Email body entered by the user
    tone = models.CharField(max_length=50)  # Tone selected by the user
    writing_style = models.CharField(max_length=50)  # Writing style selected by the user
    ai_generated_reply = models.TextField()  # AI-generated reply
    edited_reply = models.TextField(blank=True, null=True)  # User-edited reply
    save_as = models.CharField(max_length=255, blank=True, null=True)  # User-defined 'save as' name for the reply
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of when the reply was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp of the last update

    def __str__(self):
        return f"Email Reply by {self.user.username} on {self.created_at}"