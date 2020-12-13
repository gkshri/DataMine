import time
import json
data={}
Filepath="D:/demo.json"
def filecreate(Filepath="D:/demo.json"):
    print("enter file path")
    Filepath=input()

def write(data):
    f=open(Filepath,"w")
    json_object = json.dumps(data, indent = 4)
    f.write(json_object)
    print("Changes commited")
    f.close()

def create(key,value,timeout=0):
    if key in data:
        print("error: this key already exists")
    else:
        if(key.isalpha()):
            if len(data)<(1024*1020*1024) and value<=(16*1024*1024):
                if timeout==0:
                    l=[value,timeout]
                else:
                    l=[value,time.time()+timeout]
                if len(key)<=32:
                    data[key]=l
                    print("Created")
                    write(data)
                    print("File modified")
            else:
                print("large file")
        else:
            print("invalid key")
def delete(key):
    if key not in data:
        print("value not found")
    else:
        b=data[key]
        if b[1]!=0:
            if time.time()<b[1]:
                del data[key]
                print("successfully deleted")
                write(data)
                print("File modified")
            else:
                print("expired")
        else:
            del data[key]
            print("successfully deleted")        
def read(key):
    if key not in data:
        print("value not found")
    else:
        b=data[key]
        if b[1]!=0:
            if time.time()<b[1]:
                stri=str(key)+":"+str(b[0])
                return stri
            else:
                print("expired")
        else:
            stri=str(key)+":"+str(b[0])
            return stri

# filecreate()
# create("abc",10)
# create("bat",20)
# print(read("bat"))
# delete("abc")

    
