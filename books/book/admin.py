from django.contrib import admin
from .models import Book, CustomUser, BookComments, BorrowedBook
# Register your models here.

class CommentAdmin(admin.ModelAdmin):
	list_display = ('author', 'book', 'content','date_added', 'date_updated', 'active')
	list_filter = ('active', 'date_added', 'date_updated')
	search_fields = ('author', 'content')

class BorrowedAdmin(admin.ModelAdmin):
	list_display = ('book', 'borrower', 'get_status','date_borrow', 'return_date')
	list_filter = ('date_borrow', 'return_date')
	search_fields = ('borrower', 'book')

	def get_status(self, obj):
		return obj.book.status
	

class BookAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'author', 'location', 'status', 'user', 'date_added', 'date_updated')
	list_filter = ('date_added',)
	search_fields = ('title', 'status')

admin.site.register(CustomUser)
admin.site.register(Book, BookAdmin)
admin.site.register(BookComments, CommentAdmin)
admin.site.register(BorrowedBook, BorrowedAdmin)