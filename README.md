

# STEPS

1) user registraion


-> Initially users (both candidates and Interviewer) need to register in the application
-> For the candidate is_superuser of auth user table will be 1 and for candidates it will be 0
-> need to post user registration  api (http://127.0.0.1:8000/register/) 
-> sample body is shown below ,is_hr will be 1 for the interviewer and it will be 0 for candidates,it will be stored in the      is_superuser filed of auth user table as mentioned above


# candidates
{
    "username" :"Candidate1",
    "email" :"fanishmuhadds@gmail.com",
    "password" :"fanish@123",
    "password2" :"fanish@123",
    "is_hr" :"0"
    
}


# interviewr
{
    "username" :"HR2",
    "email" :"fanishmuhadds@gmail.com",
    "password" :"fanish@123",
    "password2" :"fanish@123",
    "is_hr" :"1"
    
}


2) slot registration

-> for the slot registration needed to post api api (http://127.0.0.1:8000/slot-register/)
-> sample body is shown below
-> user_Id should be valid (should be available in the user table)
{
    "user_id" :"14",
    "slot_date" : "2022-04-23",
    "from_time" : "11:00:00",
    "to_time" : "13:00:00"
}


3)get slots

->date,candidate_id,interviewr_id should be passed as parameter

-> sample url is given below
   http://127.0.0.1:8000/slots?date=2022-04-23&c_id=13&i_id=14

->c_id is candidate id and i_id is interviewr id


# ASSUMPTIONS

-> Each users must have oly 1 slot in day
-> inter view time duration is set as 10 min in the code
-> database used is sqlite3 











