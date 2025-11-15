from django.db import models

class Profile(models.Model):
    supabase_id = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username