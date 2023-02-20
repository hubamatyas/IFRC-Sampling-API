from django.db import models

# Create your models here.
class State(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    parent_state = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    term = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.name

class Option(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    child_state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, related_name='child_state')

    def __str__(self):
        return self.name