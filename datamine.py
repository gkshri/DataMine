import time
import json
import threading,_thread
from functools import partial
class datamine:
    def __init__(self):
        self.data={}
        self.Filepath="D:/demo.json"
    def filecreate(self,Filepath="D:/demo.json"):
        print("enter file path")
        self.Filepath=input()

    def write(self,data):
            f=open(self.Filepath,"w")
            json_object = json.dumps(self.data, indent = 4)
            f.write(json_object)
            print("Changes commited")
            f.close()

    def create(self,key,value,timeout=0):
            if key in self.data:
                print("error: this key already exists")
            else:
                if(key.isalpha()):
                    if len(self.data)<(1024*1020*1024) and value<=(16*1024*1024):
                        if timeout==0:
                            l=[value,timeout]
                        else:
                            l=[value,time.time()+timeout]
                        if len(key)<=32:
                            self.data[key]=l
                            print("Created")
                            d=datamine()
                            d.write(self.data)
                            print("File modified")
                        else:
                            print("large file")
                else:
                    print("invalid key")
    def delete(self,key):
            if key not in self.data:
                print("value not found")
            else:
                b=self.data[key]
                if b[1]!=0:
                    if time.time()<b[1]:
                        del self.data[key]
                        print("successfully deleted")
                        d=datamine()
                        d.write(self.data)
                        print("File modified")
                    else:
                        print("expired")
                else:
                    del self.data[key]
                    print("successfully deleted")        
    def read(self,key):
            if key not in self.data:
                print("value not found")
            else:
                b=self.data[key]
                if b[1]!=0:
                    if time.time()<b[1]:
                        stri=str(key)+":"+str(b[0])
                        return stri
                    else:
                        print("expired")
                else:
                    stri=str(key)+":"+str(b[0])
                    return stri
d=datamine()
mylock = threading.Lock()
d.filecreate()
d.create("abc",10)
d.create("bat",20)
print(d.read("bat"))
d.delete("abc")

    
