from django.contrib import admin

from .models import CustomUser, Category, Genre, Title, GenreTitle, Review, Comment


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    search_fields = ('username', 'email', 'role', 'bio')
    list_filter = ('role', 'is_superuser')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name', 'slug',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name', 'slug',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    pass
    list_display = ('name', 'year', 'category')
    search_fields = ('name', 'category', 'description')
    list_filter = ('year', 'category')


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'score', )
    search_fields = ('text', )
    list_filter = ('author', 'score', )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', )
    list_filter = ('author', )
