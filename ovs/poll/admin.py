from django.contrib import admin
from .models import Registration,Candidate,Position
# Register your models here.
#admin.site.register(Registration)
@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user','First_name','Last_name','dob')
# admin.site.register(Candidate)
admin.site.register(Position)
@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('full_name','position')
    list_filter = ('position',)
    search_fields = ('full_name','position')
    readonly_fields = ('total_vote',)
