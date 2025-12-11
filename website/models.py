from django.db import models

class Profile(models.Model):
    supabase_id = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    wrong_questions_amt = models.IntegerField(null=False, default=0)

    def __str__(self):
        return self.username
    

class Quizzes(models.Model):
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    correct_count = models.IntegerField(null=False)
    total_questions = models.IntegerField(null=False)
    accuracy = models.FloatField(null=False)


class WrongQuestions(models.Model):
    user_id = models.CharField(max_length=255)
    quiz_id = models.ForeignKey(Quizzes, on_delete=models.CASCADE)
    wrong_questions_data = models.JSONField(null=False)
