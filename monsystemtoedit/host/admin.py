from django.contrib import admin 
from .models import Members,all_users_data,agents

# Register your models here.

admin.site.register(Members)
admin.site.register(all_users_data)
admin.site.register(agents)




