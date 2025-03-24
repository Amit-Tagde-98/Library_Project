from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from book.models import *
from book import util
from book.serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout


class SignInView(APIView):
    def post(self, request):
        try:
            data = request.data
            email = data.get('email').lower()
            password = data.get('password')
            user = UserAuth.objects.filter(email=email).first()    

            user_auth = authenticate(request, email=email, password=password)
            
            if user_auth is not None:
                refresh = RefreshToken.for_user(user_auth)
                refresh_token = str(refresh)
                access_token = str(refresh.access_token)
                user_data = UserAuthSerializers(user_auth).data
               
                user.last_login = datetime.utcnow().replace(tzinfo=timezone.utc)
                
                user.save()
                
                response_data = {
                    'token': {
                        'refresh': refresh_token,
                        'access': access_token,
                    },
                    "user_data": user_data,
                    
                }
                
                return Response(util.success(self, response_data,'Login successful'))
            else:
                return Response(util.error(self, "Invalid credentials",'Invalid credentials'))
        except Exception as e:
            return Response(util.error(self, "Please check email/password",'Please check email/password'))


class SignUpView(APIView):

    def post(self, request):
        try:
            data = request.data
            email_address = data.get('email').lower()
            password = data.get('password')
            confirm_password = data.get('confirm_password')

            if not email_address or not password or not confirm_password:
                return Response(util.error(self, "All fields are required.", "All fields are required."))

            if password != confirm_password:
                return Response(util.error(self, "Password and confirm password do not match.", "Password and confirm password do not match."))

            if UserAuth.objects.filter(email=email_address).exists():
                return Response(util.error(self, "A user already exists with this email address.", "A user already exists with this email address."))

            new_user = UserAuth.objects.create_user(
                email=email_address,
                password=password,
                is_active=True
            )

            if new_user is not None:
                refresh = RefreshToken.for_user(new_user)
                response_data = {
                    'token': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    },
                    "user_data": {"email": new_user.email, "is_active": new_user.is_active}
                }
                return Response(util.success(self, response_data, "Registration successful"))

            return Response(util.error(self, "Registration failed. Please try again.", "Registration failed. Please try again."))
        except Exception as e:
            return Response(util.error(self, str(e), "An error occurred during registration."))


class LogoutView(APIView):
    def post(self, request):
        try:
            logout(request)
            return Response(util.success(self, "Log out successful","Log out successful"))

        except Exception as e:
            return Response(util.error(self, "Error during logout","Error during logout"))

class BookManageView(APIView):

    # Get all Data or while specific data using ID (GET)
    def get(self, request, format=None, id=None):
        try:
            if id is None:
                books = Book.objects.filter(is_deleted=False)
                serializer = BookSerializers(books, many=True).data
                return Response(util.success(self, serializer, "Books retrieved successfully"))
            else:
                if Book.objects.filter(id=id, is_deleted=False).exists():
                    book = Book.objects.get(id=id)
                    serializer = BookSerializers(book).data
                    return Response(util.success(self, serializer, "Book retrieved successfully"))
                else:
                    return Response(util.error(self, "Book ID not found", "The provided book ID does not exist or has been deleted."))
        except Exception as e:
            return Response(util.error(self, str(e), "An error occurred while retrieving the book."))

    # Create a book entry (POST) 
    def post(self, request):
        try:
            data = request.data
            title = data.get('title')
            author = data.get('author')
            copies = data.get('copies', 0)

            if not title or not author:
                return Response(util.error(self, "Title and author are required", "Please provide both title and author to create a book."))

            book = Book.objects.create(title=title, author=author, copies=copies)
            return Response(util.success(self, "Book created successfully", "Book created successfully"))
        
        except Exception as e:
            return Response(util.error(self, str(e), "An error occurred while creating the book."))
        
    # Update a Book (PUT)
    def put(self, request, id=None):
        try:
            if not id:
                return Response(util.error(self, "Book ID is required for update", "Book ID is missing. Please provide a valid ID."))

            book = Book.objects.filter(id=id, is_deleted=False).first()

            if not book:
                return Response(util.error(self, "Book not found", "No book found with the given ID."))

            data = request.data
            book.title = data.get('title', book.title)
            book.author = data.get('author', book.author)
            book.copies = data.get('copies', book.copies)

            book.save()
            return Response(util.success(self, "Book updated successfully", "Book updated successfully"))
        
        except Exception as e:
            return Response(util.error(self, str(e), "An error occurred while updating the book."))


    # Delete a Book (DELETE)
    def delete(self, request, id=None):
        try:
            if not id:
                return Response(util.error(self, "Book ID is required for deletion", "Book ID is missing. Please provide a valid ID."))

            book = Book.objects.filter(id=id, is_deleted=False).first()

            if not book:
                return Response(util.error(self, "Book not found", "No book found with the given ID."))

            book.is_deleted = True
            book.save()
            return Response(util.success(self,"Book deleted successfully", "Book deleted successfully"))

        except Exception as e:
            return Response(util.error(self, str(e), "An error occurred while deleting the book."))
