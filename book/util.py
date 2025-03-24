from rest_framework import status
from django.utils import timezone
import random
from datetime import datetime, timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from book.models import UserAuth
# from apps.userapp.notification import EmailNotification

def success(self, msg, status_message=None):
    response = {
                    "status_message": status_message,
                    "message": msg,
                    "status" : "success",
                    "code"   : status.HTTP_200_OK
                }
    return response

 
def error(self, msg, status_message=None):
    response = {
                    "status_message": status_message,
                    "message": msg,
                    "status" : "failed",
                    "code"   : status.HTTP_400_BAD_REQUEST
                }
    return response

 
def loginsuccess(self, msg,statuss, ):
    response = {
                    "message": msg,
                    "status" : "success",
                    "code"   : status.HTTP_200_OK,
                    "verify_status": statuss
                }
    return response

 
def loginerror(self, msg,statuss):
    response = {
                    "message": msg,
                    "status" : "failed",
                    "code"   : status.HTTP_400_BAD_REQUEST,
                    "verify_status": statuss
                }
    return response

 