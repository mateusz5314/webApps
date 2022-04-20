from django.contrib import admin


from .models import Table, User, Task

admin.site.register(User)
admin.site.register(Table)
admin.site.register(Task)
