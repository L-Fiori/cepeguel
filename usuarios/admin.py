from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from usuarios.models import Usuario

class UsuarioAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'nusp', 'date_joined', 'last_login', 'is_admin', 'is_atleta', 'is_professor', 'is_able_to_rent')
    search_fields = ('email', 'first_name', 'nusp', 'is_professor', 'is_staff')
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('email',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Usuario, UsuarioAdmin)