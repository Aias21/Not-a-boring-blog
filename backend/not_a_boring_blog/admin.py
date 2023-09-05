from django.contrib import admin
from .models.comment import Comment, ReplyComment
from .models.post import Post, Category
from .models.user import Role

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_categories', 'created_at', 'last_updated', 'status')
    list_filter = ('category__category_name', 'status')
    search_fields = ('title', 'body', 'description')

    def get_categories(self, obj):
        return ", ".join([category.category_name for category in obj.category.all()])
    get_categories.short_description = 'Category'


admin.site.register(Comment)
admin.site.register(ReplyComment)
admin.site.register(Category)
admin.site.register(Role)
admin.site.register(Post, PostAdmin)