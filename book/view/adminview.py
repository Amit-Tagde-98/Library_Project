from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from book.models import *
from django.core.paginator import Paginator
from django.db.models import Q


# Create your views here.



# @login_required
# def index(request):
#     books = Book.objects.filter(is_deleted=False).order_by('-created_at')
#     paginator = Paginator(books, 5)  # Show 5 books per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     context = {'page_obj': page_obj}

#     return render(request,'index.html',context)


# def home(request):
#     books = Book.objects.filter(is_deleted=False).order_by('-created_at')
#     paginator = Paginator(books, 5)  # Show 5 books per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     return render(request, 'home.html', {'page_obj': page_obj})

@login_required
def index(request):
    query = request.GET.get('q')
    books = Book.objects.filter(is_deleted=False).order_by('-created_at')

    if query:
        books = books.filter(Q(title__icontains=query) | Q(author__icontains=query))

    paginator = Paginator(books, 5)  # Show 5 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'page_obj': page_obj, 'query': query}
    return render(request, 'index.html', context)

def home(request):
    query = request.GET.get('q')
    books = Book.objects.filter(is_deleted=False).order_by('-created_at')

    if query:
        books = books.filter(Q(title__icontains=query) | Q(author__icontains=query))

    paginator = Paginator(books, 5)  # Show 5 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {'page_obj': page_obj, 'query': query})


def signin(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']

        user=auth.authenticate(email=email,password=password)

        if user is not None:
            auth.login(request,user)
            messages.success(request, 'Login successful!')
            return redirect('/index')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    
    return render(request,'signin.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password == cpassword:
            if UserAuth.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists. Please try a different email.')
                return redirect('/signup')
            else:
                UserAuth.objects.create_user(email=email, password=password)
                messages.success(request, 'Account created successfully! You can now log in.')
                return redirect('/index')
        else:
            messages.error(request, 'Passwords do not match. Please try again.')
            return redirect('/signup')

    return render(request, 'signup.html')

@login_required
def signout(request):
    auth.logout(request)
    messages.success(request, 'Your Account has been log out successfully!')
    return redirect('/')



@login_required
def bookform(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        copies = int(request.POST['copies'],0)
        Book.objects.create(title=title, author=author, copies=copies)
        messages.success(request, 'Book entry created successfully.')
        return redirect('/index')
    return render(request, 'bookform.html')

# Soft delete a book
@login_required
def deletebook(request, id):
    data = Book.objects.get(id=id)
    data.is_deleted = True
    data.save()
    messages.success(request, 'Book entry deleted successfully.')
    return redirect('/index')

# Update book details
@login_required
def updatebook(request, id):
    data = Book.objects.get(id=id)  # Fetch book data
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        copies = int(request.POST['copies'])
        data.title = title
        data.author = author
        data.copies = copies
        
        data.save()
        messages.success(request, 'Book entry updated successfully.')
        return redirect('/index')
    
    context = {'data': data}
    return render(request, 'updatebook.html', context)