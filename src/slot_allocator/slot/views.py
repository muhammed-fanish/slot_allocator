from datetime import datetime,timedelta
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import UserSlot
from .serializers import UserRegisterSerializer,UserSlotSerializer
from rest_framework import status
from django.contrib.auth import get_user_model
User = get_user_model()
# from rest_framework.permissions import AllowAny



# Create your views here.
class register(APIView) :
    # permission_classes = (AllowAny,)
    def post(self, request,format=None) :
        serializer = UserRegisterSerializer(data=request.data)
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
        resp = None
        error_message = None
        serializer = UserSlotSerializer(data=request.data)
        if serializer.is_valid():
            print("SERIALISER VALID")
            user_id = serializer.data['user_id']
            slot_date = serializer.data['slot_date']
            from_time = serializer.data['from_time']
            to_time = serializer.data['to_time']
            if User.objects.filter(id=user_id).exists():
                print("USER EXIST WITH ID")
                user_instance = User.objects.get(id=user_id) 
                user_slot = UserSlot.objects.create(
                    user = user_instance,
                    slot_date = slot_date,
                    from_time = from_time,
                    to_time = to_time
                )  
                print(user_slot,"USERSLOTTTTTT")
                user_slot.save() 
                resp ={
                    "status" :"Time slot booked Success fully",
                    "slot_date" : slot_date,
                    "from_time" : from_time,
                    "to_time" : to_time
                }   
            else:
                print("USER NOT EXIST WITH GIVEN ID")
                error_message = "user does not exist"
                resp = {
                    'error_message' : error_message
                }
                return Response(resp,status=404) 
                
        else :
            error_message = serializer.errors
            print(error_message,"error_MESSAGE")
            resp = {
                'error_message' : error_message
            }
            return Response(resp,status=500) 
        return Response(resp,status=status.HTTP_200_OK) 




class get_slots(APIView) :
    def get(self,request) :
        c_user = None
        i_user = None
        c_slot = None
        i_slot = None

        slot_date = request.query_params.get('date')
        c_id = request.query_params.get('c_id')
        i_id = request.query_params.get('i_id')
        if User.objects.filter(id=c_id).exists() :
            c_user = User.objects.get(id=c_id)
        if User.objects.filter(id=i_id).exists() :
            i_user = User.objects.get(id=i_id)

        if UserSlot.objects.filter(slot_date=slot_date).filter(user=c_user).exists():
            c_slot = UserSlot.objects.filter(slot_date=slot_date).filter(user=c_user)[0]
        if UserSlot.objects.filter(slot_date=slot_date).filter(user=i_user).exists():
            i_slot = UserSlot.objects.filter(slot_date=slot_date).filter(user=i_user)[0]

        if c_slot is None or i_slot is None :
            return Response({" No slots available for these users :("})
        else :
            slot_date_year = int(c_slot.slot_date.strftime("%Y"))
            slot_date_month = int(c_slot.slot_date.strftime("%m"))
            slot_date_day = int(c_slot.slot_date.strftime("%d"))
            i_slot_from_time_hour = int(i_slot.from_time.strftime("%H"))
            i_slot_from_time_min = int(i_slot.from_time.strftime("%M"))
            i_slot_from_time_sec = int(i_slot.from_time.strftime("%S"))
            i_slot_to_time_hour = int(i_slot.to_time.strftime("%H"))
            i_slot_to_time_min = int(i_slot.to_time.strftime("%M"))
            i_slot_to_time_sec = int(i_slot.to_time.strftime("%S"))
            c_slot_from_time_hour = int(c_slot.from_time.strftime("%H"))
            c_slot_from_time_min = int(c_slot.from_time.strftime("%M"))
            c_slot_from_time_sec = int(c_slot.from_time.strftime("%S"))
            c_slot_to_time_hour = int(c_slot.to_time.strftime("%H"))
            c_slot_to_time_min = int(c_slot.to_time.strftime("%M"))
            c_slot_to_time_sec = int(c_slot.to_time.strftime("%S"))


            i_slot_start_time = datetime(slot_date_year, slot_date_month, slot_date_day, i_slot_from_time_hour, i_slot_from_time_min, i_slot_from_time_sec, 000000)
            i_slot_end_time = datetime(slot_date_year, slot_date_month, slot_date_day, i_slot_to_time_hour, i_slot_to_time_min, i_slot_to_time_sec, 000000)
            c_slot_start_time = datetime(slot_date_year, slot_date_month, slot_date_day,c_slot_from_time_hour,c_slot_from_time_min,c_slot_from_time_sec, 000000)
            c_slot_end_time = datetime(slot_date_year, slot_date_month,slot_date_day,c_slot_to_time_hour,c_slot_to_time_min,c_slot_to_time_sec, 000000)

            is_conflict = check_time_conflict(i_slot_start_time,i_slot_end_time,c_slot_start_time,c_slot_end_time)
            if is_conflict :
                time_slot_list =[i_slot_start_time,i_slot_end_time,c_slot_start_time,c_slot_end_time]
                time_slot_list.sort()
                conflict_from_time = time_slot_list[1]
                conflict_to_time = time_slot_list[2]
                available_slot = []
                interview_duration = 10 # in minutes 
                interview_time = []
                while(conflict_from_time < conflict_to_time) :
                    new_conflict_from_time = conflict_from_time + timedelta(minutes=interview_duration)
                    if new_conflict_from_time < conflict_to_time :
                        interview_time.append([conflict_from_time.strftime("%H:%M:%S"),new_conflict_from_time.strftime("%H:%M:%S")])
                    conflict_from_time = new_conflict_from_time
            
                if len(interview_time)> 0 :
                    available_slot.append(interview_time)
                resp ={
                    "Date": slot_date,
                    "Availabe Slots" : available_slot
                }

                return Response(resp,status=200)
                
                    









            


    
def check_time_conflict(i_slot_start_time,i_slot_end_time,c_slot_start_time,c_slot_end_time) :
    is_conflict = False
    delta = max(i_slot_start_time,c_slot_start_time) - min(i_slot_end_time,c_slot_end_time)
    if delta.days < 0 :
       is_conflict = True
    return is_conflict




