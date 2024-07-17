from django.db import models

class LinkData(models.Model):
    link = models.CharField(max_length=255, unique=True)
    bw = models.FloatField()
    delay = models.CharField(max_length=50)
    loss = models.FloatField()
    jitter = models.CharField(max_length=50)
    error = models.FloatField()
    max_queue_size = models.IntegerField()
    rate = models.FloatField()
    mtu = models.IntegerField()
    timestamp = models.DateTimeField()
    
    def __str__(self):
        return self.link
