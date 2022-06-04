from django.contrib import admin


from .models import Table, User, Task, List

admin.site.register(User)
admin.site.register(Table)
admin.site.register(List)
admin.site.register(Task)
