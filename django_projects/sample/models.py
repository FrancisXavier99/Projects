from django.db import models

class Member(models.Model):
    firstname=models.CharField(max_length=30)
    lastname=models.CharField(max_length=30)
    email=models.EmailField(max_length=254)
    password=models.CharField(max_length=120)
 
    def __str__(self):
        return self.firstname + " " + self.lastname

   	
    class Meta:  
        db_table = "login_form"
		
