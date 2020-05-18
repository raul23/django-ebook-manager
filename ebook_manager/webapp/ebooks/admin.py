from django.contrib import admin

# Register your models here.
from .models import Author, Book, BookFile, Category, Rating, Tag


def init_var(var):
    return [] if var is None else var


def get_fields_to_display(model, beginning=None, ending=None, readonly=None,
                          exclude=None):
    # TODO: find better way
    # TODO: accessing protected attribute _meta
    meta = getattr(model, '_meta', None)
    if meta is None:
        raise AttributeError("model {} doesn't have the attribute _meta".format(model))
    all_fields = getattr(meta, 'fields', None)
    if all_fields is None:
        raise AttributeError("model {} doesn't have the attribute fields".format(model))
    beginning = init_var(beginning)
    ending = init_var(ending)
    readonly = init_var(readonly)
    exclude = init_var(exclude)
    fields_to_keep = []
    ignore_fields = []
    ignore_fields.extend(beginning)
    ignore_fields.extend(ending)
    ignore_fields.extend(readonly)
    ignore_fields.extend(exclude)
    if beginning:
        fields_to_keep.extend(beginning)
    for field_obj in all_fields:
        if 'AutoField' in str(type(field_obj)):
            continue
        if hasattr(field_obj, 'editable') and not field_obj.editable:
            continue
        field_name = str(field_obj).split('.')[-1]
        if field_name not in ignore_fields:
            fields_to_keep.append(field_name)
    # Readonly fields are added at the end of the list of fields to display
    if readonly:
        fields_to_keep.extend(readonly)
    if ending:
        fields_to_keep.extend(ending)
    return fields_to_keep


class BookAdmin(admin.ModelAdmin):
    exclude = ('isbn10', 'isbn13', 'asin',)
    fields = get_fields_to_display(
        model=Book,
        ending=['book_format', 'thumbnail_cover_image', 'enlarged_cover_image'],
        exclude=exclude)


class BookFileAdmin(admin.ModelAdmin):
    readonly_fields = ('isbn10', 'isbn13', 'asin', 'size', 'md5', 'sha256',)
    exclude = ('book_format',)
    fields = get_fields_to_display(
        model=BookFile,
        beginning=['title', 'file_path', 'books'],
        readonly=readonly_fields,
        exclude=exclude)


admin.site.register(Author)
admin.site.register(Book, BookAdmin)
admin.site.register(BookFile, BookFileAdmin)
admin.site.register(Category)
admin.site.register(Rating)
admin.site.register(Tag)
