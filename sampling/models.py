from django.db import models

# Create your models here.
class State(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    parent_id = models.IntegerField(null=True)
    description = models.TextField(max_length=5000, null=True)

    def __str__(self):
        return self.name

class Option(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    option = models.CharField(max_length=100)
    child_state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='child_id', null=True)

    def __str__(self):
        return self.option