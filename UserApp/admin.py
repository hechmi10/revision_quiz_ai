from django.contrib import admin

from UserApp.models import User
from UserApp.models import AdminUser
from UserApp.models import InstructorUser
from UserApp.models import StudentUser
# Register your models here.
admin.site.register(User)

admin.site.register(AdminUser)

admin.site.register(InstructorUser)

admin.site.register(StudentUser)
