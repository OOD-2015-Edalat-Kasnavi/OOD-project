from django.contrib import admin
import users.models
import knowledge.models
# Register your models here.

admin.site.site_header = 'K knowledge management system'
admin.site.register(users.models.KUser)
admin.site.register(users.models.ReportAbuseRequest)
admin.site.register(users.models.SpecialPrivilegeRequest)
admin.site.register(knowledge.models.Knowledge)
admin.site.register(knowledge.models.Source)
admin.site.register(knowledge.models.TagType)
admin.site.register(knowledge.models.Tag)
admin.site.register(knowledge.models.InterknowledgeRelationshipType)
admin.site.register(knowledge.models.InterknowledgeRelationship)
admin.site.register(knowledge.models.Comment)
