from django.contrib import admin
from .models.comment import Comment, ReplyComment
from .models.post import Post, Category
from .models.user import Role
from .models.views import View


class RoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_blogger', 'is_moderator', 'is_admin')
    list_filter = ('is_blogger', 'is_moderator', 'is_admin')


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_categories', 'created_at', 'last_updated', 'status')
    list_filter = ('category__category_name', 'status')
    search_fields = ('title', 'body', 'description')

    def get_categories(self, obj):
        return ", ".join([category.category_name for category in obj.category.all()])
    get_categories.short_description = 'Category'


admin.site.register(View)
admin.site.register(Comment)
admin.site.register(ReplyComment)
admin.site.register(Category)
admin.site.register(Role, RoleAdmin)
admin.site.register(Post, PostAdmin)