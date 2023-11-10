from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200, default='')
    description = models.TextField(blank=True)
    done = models.BooleanField(default=False)

    def __str__(self) -> str:        
        return self.title
