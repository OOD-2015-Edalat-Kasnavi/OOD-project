from django.contrib import admin
import users.models
import knowledge.models
# Register your models here.

admin.site.site_header = 'K knowledge management system'
admin.site.register(users.models.KUser)
admin.site.register(knowledge.models.Knowledge)
admin.site.register(knowledge.models.Source)
