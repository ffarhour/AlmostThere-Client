"""

.. module: GPS Analysis - OutputAPI
.. moduleauthor: Farmehr Farhour f.farhour@gmail.com

"""
#import threading
import threading
import time

class User:
    #User class to define the attributes for each user
    usercount = 0
    def __init__(self, DeviceID, Latitude, Longitude, DateTime):
        self.DeviceID = DeviceID
        self.Latitude = Latitude
        self.Longitude = Longitude
        self.DateTime = DateTime
        User.usercount += 1

#define 10 uers as objects in a list
userlist = []
DevID = 1
for a in range(1,11):
    userlist.append(User(DevID,-35,45,time.time()))
    DevID +=1

for a in userlist:
    print(a)


#change users 1-10 position every 10 seconds
def changeposition():
    threading.Timer(10.0,changeposition).start()
    for a in range(0,10):
        userlist[a].Latitude += 0.1
        userlist[a].Longitude -= 0.1
        userlist[a].DateTime = time.time()
    for b in range(0,10):
        print("print of userlist of 10 users", userlist[b].Latitude,userlist[b].Longitude,userlist[b].DateTime)
changeposition()

'''
#change user1 position every 10 seconds
def changeposition():
    threading.Timer(10.0, changeposition).start()
    userlist[0].Latitude += 1
    userlist[0].Longitude -=1
    userlist[0].DateTime = time.time()
    print(userlist[0].Latitude,userlist[0].Longitude,userlist[0].DateTime)

changeposition()
'''

#define lists to collect userdata
class lists:
    def __init__(self, LatList, LongList, TimeList,x):
        self.LatList = LatList
        self.LongList = LongList
        self.TimeList = TimeList
        self.x = x

    #collects and stores user's data every 30 seconds
    def obtainposition(self):
        self.LatList.append(userlist[self.x].Latitude)
        self.LongList.append(userlist[self.x].Longitude)
        self.TimeList.append(userlist[self.x].DateTime)

    #delets appended points less than 1 unit from previous point
    def distmoved(self):
        #counts  number of entries in lists
        x = len(self.TimeList)
        print("x",x)
        #deletes the points within 1 unit circle of the previous point. Will not delete the initial point.
        if x>1:
            distx = abs(self.LongList[x-1]) - abs(self.LongList[x-2])
            disty = abs(self.LatList[x-1]) - abs(self.LatList[x-2])
            if distx**2 + disty**2 <= 1:
                del self.LongList[x-1]
                del self.LatList[x-1]
                del self.TimeList[x-1]
'''
    def distmoved(self):
        x = len(self.LongList)
        y = len(self.LatList)
        while x==y:
            if x>2:
                distx = abs(self.LongList[x]) - abs(self.LongList[x])
                disty = abs(self.LatList[y]) - abs(self.LatList[y])
                if distx**2 + disty**2 < 1:
                    self.LongList.remove[x-1]
                    self.LatList.remove[y-1]
                    self.TimeList.remove[y-1]

'''


#create list1 object for user1
list1 = lists([],[],[],0)

#append lists every 30 seconds
def listappend():
    threading.Timer(30.0,listappend).start()
    list1.obtainposition()
    list1.distmoved()
    print("print of appended data list for user1",list1.LatList,list1.LongList,list1.TimeList)

listappend()

