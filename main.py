from os import sep
from os import path
from instagrapi import Client # https://github.com/adw0rd/instagrapi
import time
from datetime import datetime

user_to_observe = input("Username to track: ")
username = input("Your account login: ")
password = input("Your account password: ")

log_file = path.dirname(__file__) + "\\follower.log"

def log(message):
    with open(log_file, "a+") as f:
        f.write(message + "\n")

def currentTime():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S") + " - "

cl = Client()

try:
    cl.login(username, password)
except: 
    print(currentTime() + "Failed to login, please restart application")
    time.sleep(10)
    quit()

user_id = cl.user_id_from_username(user_to_observe)

def dictToList(dict):
    return_list = []

    for key, value in dict:
        return_list.append(value.username)

    return return_list

print(currentTime() + "Fetching Followers and Following")
global_followers = dictToList(cl.user_followers(user_id).items())
global_following = dictToList(cl.user_following(user_id).items())
print(currentTime() + "Fetched!")


# Check if the lists have differences
# If so sort them
def checkLists(new_list, old_list):
    new_follower = []
    new_unfollow = []
    
    for user in new_list:
        if user in old_list:
            continue
        if user not in old_list:
            log (currentTime() + "new follower - " + user)
            new_follower.append(user)
    
    for user in old_list:
        if user in new_list:
            continue
        if user not in new_list:
            log(currentTime() + "new unfollow - " + user)
            new_unfollow.append(user)
    
    return new_follower, new_unfollow


while True:
    print(currentTime() + "Checking in 60 seconds")
    time.sleep(60)
    print(currentTime() + "Checking now")
    temp_follower = dictToList(cl.user_followers(user_id, False).items())
    temp_following = dictToList(cl.user_following(user_id, False).items())
    print(currentTime() + "Len Follower " + str(len(temp_follower)), "Len Following " + str(len(temp_following)), sep=" ")
    print(currentTime() + "Fetched new Lists")
    result_follower = checkLists(temp_follower, global_followers)
    result_following = checkLists(temp_following, global_following)

    global_followers = temp_follower
    global_following = temp_following


    print(currentTime() + "New followers: " + str(result_follower[0]), "New unfollower: " + str(result_follower[1]), sep=" ")
    print(currentTime() + "New following: " + str(result_following[0]), " New unfollowed: " + str(result_following[1]), sep=" ")
