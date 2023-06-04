from urllib.parse import quote_plus
from pymongo import MongoClient

# MongoDB connection string
user=quote_plus("PASSWORD")

client=MongoClient("URL")
db=client["login_info"]
col=db["login0"]

#Validate email and password
def validate(email,password): 
    if email and password:
        data=data=col.find_one({"email":email,"password":password})
        if data:
            return True
        else:
            return False
    else:
        return False
    
#Insert data into database
def insert(name,email,password,disability,role,dob,slink,glink,llink,bio,gender): 
    if name and check(email) and password and disability and role:
        query={"name":name,
               "email":email,
               "password":password,
               "disability":disability,
               "role":role,
               "dob":dob,
               "slink":slink,
               "glink":glink,
               "llink":llink,
               "bio":bio,
               "gender":gender}
        col.insert_one(query)
        return True
    else:
        return False
    
#Update data in database
def update(name,email,disability,role,dob,slink,llink,glink,bio,gender):
    if not check(email):
        if name and email :
            col.update_many({"email":email}, {"$set":{"name":name,"disability":disability,"role":role,"dob":dob,"slink":slink,"glink":glink,"llink":llink,"bio":bio,"gender":gender}})
            return True
        else:
            return False
    else:
        return False

def updatepwd(email,password):
    if not check(email):
        if password and email :
            col.update_many({"email":email}, {"$set":{"password":password}})
            return True
        else:
            return False
    else:
        return False
    
#Check if email already exists
def check(email): 
    if email:
        data=col.find_one({"email":email})
        if data:
            return False
        else:
            return True
        
#show all data in database
def show(email): 
    if email:
        data=col.find_one({"email":email},{"_id":0})
        return data
    else:
        return False
