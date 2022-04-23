from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegister,UserSlot
# from rest_framework.permissions import AllowAny



# Create your views here.
class register(APIView) :
    # permission_classes = (AllowAny,)
    def post(self, request,format=None) :
        serializer = UserRegister(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data["response"] ="User account created successfully"
            data["username"] = account.username
            data["email"] = account.email
            data["id"] = account.id
            data["is_hr"] = account.is_superuser
            
            # token = Token.objects.get(user=account).key  
            # data["token"] = token
            
        else :
            data = serializer.errors

        return Response(data) 




class slot_register(APIView) :
    def post(self, request,format=None) :
        resp = {}
        serializer = UserSlot(data=request.data)
        if serializer.is_valid():
            user_slot = serializer.save()
            resp["response"] ="Time slot booked successfully"
            resp["user_id"] = user_slot.user.user_id
            resp["date"] = user_slot.slot_date
            resp["from_time"] = user_slot.from_time
            resp["to_time"] = user_slot.to_time
        else :
            resp = serializer.errors

        return Response(resp) 



# class get_slots(APIView) :
#     def get(self,request) :
#         date = request.query_params.get('date')
#         c_id = request.query_params.get('candidate_id')
#         i_id = request.query_params.get('interviewer_id')

        
        
#         return Response(resp) 






