from os import sep
from os import path
from instagrapi import Client # https://github.com/adw0rd/instagrapi
import time

user_to_observe = "USER TO TRACK"
username = "UR USER"
password = "UR PASSWORD"

log_file = path.dirname(__file__) + "\\follower.log"

def log(message):
    with open(log_file, "a+") as f:
        f.write(message + "\n")

cl = Client()
cl.login(username, password)

user_id = cl.user_id_from_username(user_to_observe)

def dictToList(dict):
    return_list = []

    for key, value in dict:
        return_list.append(value.username)

    return return_list

print("Fetching Followers and Following")
global_followers = dictToList(cl.user_followers(user_id).items())
global_following = dictToList(cl.user_following(user_id).items())
print("Fetched!")


# Check if the lists have differences
# If so sort them
def checkLists(new_list, old_list):
    new_follower = []
    new_unfollow = []
    
    for user in new_list:
        if user in old_list:
            continue
        if user not in old_list:
            log ("new follower - " + user)
            new_follower.append(user)
    
    for user in old_list:
        if user in new_list:
            continue
        if user not in new_list:
            log("new unfollow - " + user)
            new_unfollow.append(user)
    
    return new_follower, new_unfollow


while True:
    print("Checking in 600 seconds")
    time.sleep(600)
    print("Checking now")
    temp_follower = dictToList(cl.user_followers(user_id, False).items())
    temp_following = dictToList(cl.user_following(user_id, False).items())
    print("Len Follower " + str(len(temp_follower)), "Len Following " + str(len(temp_following)), sep=" ")
    print("Fetched new Lists")
    result_follower = checkLists(temp_follower, global_followers)
    result_following = checkLists(temp_following, global_following)

    global_followers = temp_follower
    global_following = temp_following


    print("New followers: " + str(result_follower[0]), "New unfollower: " + str(result_follower[1]), sep=" ")
    print("New following: " + str(result_following[0]), " New unfollowed: " + str(result_following[1]), sep=" ")



    







