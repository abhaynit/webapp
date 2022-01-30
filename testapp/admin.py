from django.contrib import admin
from .models import recrd

# Register your models here
@admin.register(recrd)
class entry_exit_records(admin.ModelAdmin):
    list_display = ['id','student_id','student_name','student_branch','purpose','destination','exit_time','entry_time','is_late']
