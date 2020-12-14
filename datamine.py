import time
import json
import threading,_thread
class datamine:
    Filepath="D:/demo.json"                       #File path
    def __init__(self,data={}):                   #constructor
        self.lock=threading.Lock()
        self.data=data

    def filepathcreate(self,var):
        if var=='':
            datamine.Filepath="D:/demo.json"      #default filepath
        else:
            datamine.Filepath=var
    
    def searchfromJSON(self):
            data=self.readJSON()
            d=datamine(data)
            d.read("abc")                          #use read here to read from the JSON file
            
            
    def write(self,data):                          #Write to file
            self.lock.acquire()                    #self lock for accessing the resource
            f=open(datamine.Filepath,"w")
            print("writing to file-")
            print(datamine.Filepath)
            json_object = json.dumps(self.data, indent = 4)
            f.write(json_object)
            print("Changes commited")
            self.lock.release()
            f.close()

    def readJSON(self):                            #Read a JSON file
            self.filepathcreate()
            f=open(datamine.Filepath,"r")
            data=json.load(f)
            print("reading from JSON file")
            print(data)
            return(data)

    def writeJSONobj(self,JSONobj={}):              #Write a json File to the dict
            f=open(datamine.Filepath,"a")
            print("writing JSON object to file")
            for key in JSONobj:
                b=JSONobj.get(key)
                self.create(str(key),str(b[0]),str(0))
            f.close()


    def create(self,key,value,timeout=0):           # create an entry in the JSON file, We can use TTL if needed as a 3rd param
            if key in self.data:
                print("error: this key already exists")
            else:
                if(key.isalpha()):
                    if len(self.data)<(1024*1020*1024) and value<=(16*1024*1024): # data<1GB and JSONobj < 16kb
                        if timeout==0:
                            l=[value,timeout]
                        else:
                            l=[value,time.time()+timeout]
                        if len(key)<=32:                                          # key length<32
                            self.data[key]=l
                            print("Created")
                            self.write(self.data)
                            print(self.data);
                            print("File modified")
                        else:
                            print("large file")
                else:
                    print("invalid key")

    def delete(self,key):                             # Delete an entry from the file 
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

    def read(self,key):                                 # Reading from the file
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

# create a class object to access the functions
d=datamine()
print("enter path defaults to D:/demo.json")
var=input()
d.filepathcreate(var)
d.create("abc",10,60)
d.create("bat",20)
d.readJSON()
d.searchfromJSON()
dic={'pine': [10,0]}
d.writeJSONobj(dic)
print(d.read("abc"))
print(d.read("pine"))
#d.delete("bat")
