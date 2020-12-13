import time
import json
import threading,_thread
class datamine:
    Filepath="D:/demo.json"
    def __init__(self):
        self.lock=threading.Lock()
        self.data={}

    def filepathcreate(self,var):
        if var=='':
            datamine.Filepath="D:/demo.json"
        else:
            datamine.Filepath=var

    def write(self,data):
            self.lock.acquire()
            f=open(datamine.Filepath,"w")
            print("writing to file")
            print(datamine.Filepath)
            json_object = json.dumps(self.data, indent = 4)
            f.write(json_object)
            print("Changes commited")
            self.lock.release();
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
                            self.write(self.data)
                            print(self.data);
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
                        print("data after")
                        print(self.data)
                        self.write(self.data)
                        print("File modified")
                    else:
                        print("expired")
                else:
                    del self.data[key]
                    print("else")
                    print("successfully deleted")
                    print("data after")
                    print(self.data)
                    self.write(self.data)
                    print("File modified")        
    def read(self,key):
            self.lock.acquire()
            if key not in self.data:
                print("value not found")
                self.lock.release();
            else:
                b=self.data[key]
                if b[1]!=0:
                    if time.time()<b[1]:
                        stri=str(key)+":"+str(b[0])
                        self.lock.release();
                        return stri
                    else:
                        self.lock.release();
                        print("expired")
                else:
                    stri=str(key)+":"+str(b[0])
                    print("reading")
                    self.lock.release();
                    return stri
d=datamine()
print("enter path defaults to D:/demo.json")
var=input()
d.filepathcreate(var)
d.create("abc",10,60)
d.create("bat",20)
print(d.read("abc"))
print(d.read("bat"))
d.delete("bat")
