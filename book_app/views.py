from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from django.contrib import messages



def index(request):
    return render(request, 'book_app/index.html')

def book_form(request):
    # این ویو فقط صفحه انتخاب عمل را نمایش می‌دهد
    return render(request, 'book_app/book_form.html')


def book_list(request):
    books = Book.objects.all()

    # گرفتن تمام ژانرهای منحصربه‌فرد
    genres = Book.objects.values_list('genre', flat=True).distinct()
    genres = [genre for genre in genres if genre]  # حذف مقادیر خالی

    context = {
        'books': books,
        'genres': genres,
    }
    return render(request, 'book_app/book_list.html', context=context)


def book_detail(request, pk):
    book_dt = get_object_or_404(Book, pk=pk)
    return render(request, 'book_app/book_detail.html', context={'book_dt': book_dt})

def book_create(request):
    if request.method == 'POST':
        # دریافت داده‌ها از فرم HTML
        title = request.POST.get('title')
        author = request.POST.get('author')
        genre = request.POST.get('genre')
        published_date = request.POST.get('published_date')
        is_read = request.POST.get('is_read') == 'on'  # تبدیل به boolean

        # اعتبارسنجی داده‌های اجباری
        if not title:
            messages.error(request, 'عنوان کتاب الزامی است!')
            return render(request, 'book_app/book_form.html', {
                'title': title,
                'author': author,
                'genre': genre,
                'published_date': published_date,
                'is_read': is_read,
                'form_title': 'ایجاد کتاب جدید'
            })

        if not author:
            messages.error(request, 'نویسنده کتاب الزامی است!')
            return render(request, 'book_app/book_form.html', {
                'title': title,
                'author': author,
                'genre': genre,
                'published_date': published_date,
                'is_read': is_read,
                'form_title': 'ایجاد کتاب جدید'
            })

        # بررسی تکراری بودن عنوان کتاب
        if Book.objects.filter(title=title).exists():
            messages.error(request, 'کتاب مورد نظر در حال حاضر در لیست کتاب‌ها وجود دارد! لطفاً عنوان دیگری انتخاب کنید.')
            return render(request, 'book_app/book_form.html', {
                'title': title,
                'author': author,
                'genre': genre,
                'published_date': published_date,
                'is_read': is_read,
                'form_title': 'ایجاد کتاب جدید'
            })

        try:
            # ایجاد کتاب جدید در دیتابیس
            book = Book.objects.create(
                title=title,
                author=author,
                genre=genre if genre else '',  # اگر خالی بود رشته خالی
                published_date=published_date if published_date else None,
                is_read=is_read
            )

            # پیام موفقیت
            messages.success(request, f'کتاب "{book.title}" با موفقیت ایجاد شد!')

            # هدایت به صفحه جزئیات کتاب جدید
            return redirect('book_detail', pk=book.id)

        except Exception as e:
            # مدیریت خطاهای احتمالی
            messages.error(request, f'خطا در ایجاد کتاب: {str(e)}')
            return render(request, 'book_app/book_form.html', {
                'title': title,
                'author': author,
                'genre': genre,
                'published_date': published_date,
                'is_read': is_read,
                'form_title': 'ایجاد کتاب جدید'
            })

    else:
        # برای درخواست GET - نمایش فرم خالی
        return render(request, 'book_app/book_form.html', {
            'form_title': 'ایجاد کتاب جدید',
            'title': '',
            'author': '',
            'genre': '',
            'published_date': '',
            'is_read': False
        })

def book_update(request, pk):
    # پیدا کردن کتابی که می‌خواهیم ویرایش کنیم
    book_update = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        # دریافت داده‌های جدید از فرم
        title = request.POST.get('title')
        author = request.POST.get('author')
        genre = request.POST.get('genre')
        published_date = request.POST.get('published_date')
        is_read = request.POST.get('is_read') == 'on'  # تبدیل به بولی

        # اعتبارسنجی داده‌های اجباری
        if not title:
            messages.error(request, 'عنوان کتاب الزامی است!')
            return render(request, 'book_app/book_form.html', {
                'title': title,
                'author': author,
                'genre': genre,
                'published_date': published_date,
                'is_read': is_read,
                'form_title': 'ویرایش کتاب'
            })

        if not author:
            messages.error(request, 'نویسنده کتاب الزامی است!')
            return render(request, 'book_app/book_form.html', {
                'title': title,
                'author': author,
                'genre': genre,
                'published_date': published_date,
                'is_read': is_read,
                'form_title': 'ویرایش کتاب'
            })

        try:
            # آپدیت اطلاعات کتاب
            book_update.title = title
            book_update.author = author
            book_update.genre = genre if genre else ''
            book_update.published_date = published_date if published_date else None
            book_update.is_read = is_read
            book_update.save()  # ذخیره تغییرات در دیتابیس

            # نمایش پیام موفقیت
            messages.success(request, f'کتاب "{book_update.title}" با موفقیت ویرایش شد!')

            # هدایت به صفحه جزئیات کتاب
            return redirect('book_detail', pk=book_update.pk)

        except Exception as e:
            # مدیریت خطا
            messages.error(request, f'خطا در ویرایش کتاب: {str(e)}')
            return render(request, 'book_app/book_form.html', {
                'title': title,
                'author': author,
                'genre': genre,
                'published_date': published_date,
                'is_read': is_read,
                'form_title': 'ویرایش کتاب'
            })

    else:
        # برای درخواست GET - نمایش فرم با اطلاعات فعلی کتاب
        return render(request, 'book_app/book_form.html', {
            'form_title': 'ویرایش کتاب',
            'title': book_update.title,
            'author': book_update.author,
            'genre': book_update.genre,
            'published_date': book_update.published_date.strftime('%Y-%m-%d') if book_update.published_date else '',
            'is_read': book_update.is_read
        })


def book_delete(request, pk):
    # پیدا کردن کتاب مورد نظر
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        # اگر کاربر تأیید کرد، کتاب حذف می‌شود
        try:
            book_title = book.title  # ذخیره عنوان برای پیام
            book.delete()  # حذف کتاب از دیتابیس

            messages.success(request, f'کتاب "{book_title}" با موفقیت حذف شد!')
            return redirect('book_list')  # هدایت به لیست کتاب‌ها

        except Exception as e:
            messages.error(request, f'خطا در حذف کتاب: {str(e)}')
            return redirect('book_detail', pk=pk)

    else:
        # برای درخواست GET - نمایش صفحه تأیید حذف
        return render(request, 'book_app/book_confirm_delete.html', {
            'book': book
        })


def toggle_read(request, pk):
    # پیدا کردن کتاب مورد نظر
    book = get_object_or_404(Book, pk=pk)

    try:
        # تغییر وضعیت خوانده شده
        book.is_read = not book.is_read
        book.save()

        # پیام موفقیت
        status = "خوانده شده" if book.is_read else "خوانده نشده"
        messages.success(request, f'وضعیت کتاب "{book.title}" به "{status}" تغییر کرد!')

    except Exception as e:
        # مدیریت خطا
        messages.error(request, f'خطا در تغییر وضعیت کتاب: {str(e)}')

    # هدایت به صفحه قبلی
    return redirect(request.META.get('HTTP_REFERER', 'book_list'))