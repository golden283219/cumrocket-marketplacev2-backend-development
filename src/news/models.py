from django.db import models

class Article(models.Model):

    image = models.ImageField(upload_to='images/news')
    title = models.CharField(max_length=255)
    summary = models.TextField()
    url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0} ({1})'.format(self.title, self.pk)

    class Meta:
        ordering = ['-created_at']
