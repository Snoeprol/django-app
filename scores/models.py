from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    id = models.AutoField(primary_key=True)
    
# User model with User, Date, and Score fields
class Score(models.Model):
    user = models.CharField(max_length=50)
    date = models.DateField()
    score = models.IntegerField()
    
    def __str__(self):
        return self.user
    
    class Meta:
        ordering = ['user']
        verbose_name_plural = 'users'

    @classmethod
    def create(cls, user, date, score):
        current_score = cls(user=user, date=date, score=score)
        # Check if totalscore of user exists
        if TotalScore.objects.filter(user=user).exists():
            # Get total score of user
            total_score = TotalScore.objects.get(user=user)
            # Add score to total score
            total_score.total_score += score
            # Save total score
            total_score.save()
        # Create the total score and user if it doesn't exist
        else:
            # Create id for total score
            #id = int(TotalScore.objects.count()) + 1
            total_score = TotalScore(user=user, total_score=score)
            user = User(username=user)
            user.save()
            total_score.save()
        return current_score
    
# Total scores per user
class TotalScore(models.Model):
    user = models.CharField(max_length=50)
    total_score = models.IntegerField()
    
    def __str__(self):
        return self.user
    
    class Meta:
        ordering = ['user']
        verbose_name_plural = 'users'
    