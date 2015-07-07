from django.contrib import admin
import users.models
import knowledge.models
# Register your models here.

admin.site.site_header = 'K knowledge management system'
admin.site.register(users.models.User)
admin.site.register(users.models.Manager)
admin.site.register(knowledge.models.FileKnowledge)
admin.site.register(knowledge.models.TextKnowledge)
admin.site.register(knowledge.models.Source)
