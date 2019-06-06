from django.contrib import admin
from .models import reservation
# Register your models here.
# caller
# show reservation details
# button to accept work
# show restaurant details
# button to mark call as done
# feedback after call
# restaurant info correct?
# restaurant info to add?
# send email when reservation confirmed
# send email to customer 2 hours after reservation time to get feedback
myModels = [reservation]
admin.site.register(myModels)
