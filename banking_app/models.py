from django.db import models

# Create your models here.

class regmodel(models.Model):
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    phone = models.IntegerField()
    email=models.EmailField()
    image=models.FileField(upload_to='banking_app/static')
    pin=models.CharField(max_length=20)
    balance=models.IntegerField()
    acnum=models.IntegerField()


class addamount(models.Model):
    uid = models.IntegerField()
    amount=models.IntegerField()
    date=models.DateField(auto_now=True)

class withdrawamount(models.Model):
    uid=models.IntegerField()
    amount=models.IntegerField()
    date=models.DateField(auto_now=True)

class ministatement(models.Model):
    choice=[
        ('withdraw','withdraw'),
        ('deposit','deposit'),
    ]
    statement=models.IntegerField(choices=choice)


class newsmodel(models.Model):
    topic=models.CharField(max_length=300)
    content=models.CharField(max_length=5000)
    date=models.DateField(auto_now=True)

class wishlist(models.Model):
    uid=models.IntegerField()
    newsid =models.IntegerField()
    topic = models.CharField(max_length=300)
    content = models.CharField(max_length=5000)
    date = models.DateField()