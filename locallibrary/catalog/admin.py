from django.contrib import admin

# Register your models here.

from catalog.models import Author, Genre, Book, BookInstance

# admin.site.register(Book)
# admin.site.register(BookInstance)
# admin.site.register(Author)
admin.site.register(Genre)

#superuser with username of hamidreza and 
#password of hamid123456 was established

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
admin.site.register(Author, AuthorAdmin)

class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'status','due_back' , 'get_book_name')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
         'fields':('book', 'imprint', 'id')
        }),
        ('Availability', {
         'fields':('status', 'due_back')
        }),
    )