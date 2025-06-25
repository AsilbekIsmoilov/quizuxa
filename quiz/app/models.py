from django.db import models
from accounts.models import User


class Trainer(models.Model):

    user = models.OneToOneField(User, primary_key=True,on_delete=models.CASCADE)

    class Meta:

        verbose_name = "Trainer"
        verbose_name_plural = "Trainers"

        def __str__(self):
            return f"Trainer: {self.user.username}"
        
class Intern(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='interns') 

    class Meta:
        
        verbose_name = "Intern"
        verbose_name_plural = "Interns"

    def __str__(self):
        return f"Intern: {self.user.username}"


class Question(models.Model):
    text = models.TextField(null=True)

    def __str__(self):
        return f'Question: {self.text}'
    

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'Answer: {self.text}'
    
class InternAnswer(models.Model):
    intern = models.ForeignKey(Intern, related_name='answers', on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    is_late = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.intern} → {self.answer}'


class TestResult(models.Model):
    intern = models.ForeignKey(Intern, on_delete=models.CASCADE)
    score = models.IntegerField(default=0,null=True)
    date = models.DateTimeField(auto_now_add=True)
    duration_minutes = models.CharField(max_length=250,null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    total_questions = models.IntegerField(default=10, null=True)




    def __str__(self):
        return f'{self.intern.user.username} - Score: {self.score}'
