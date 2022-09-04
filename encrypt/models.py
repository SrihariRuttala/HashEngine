from django.db import models

# Create your models here.


class Hashes(models.Model):
    plain_text = models.TextField()
    md5 = models.TextField()
    sha1 = models.TextField()
    sha224 = models.TextField()
    sha256 = models.TextField()
    sha384 = models.TextField()


class Uploads(models.Model):
    description = models.TextField()
    text_file = models.FileField(upload_to='uploads')
    date_created = models.DateTimeField(auto_now_add=True)
    updated = models.BooleanField(default=False)

    # def snippet(self):
    #     if self.updated == True:
    #         print(self.text_file)
