import requests
import json
import time
import threading

hostname = "http://127.0.0.1:5000"
choice = -1

def fetch_messages(lobby_id, secret):
    while True:
        r = requests.post(hostname + "/api/read_messages/" + lobby_id, data={"secret": secret})
        if r.status_code != 200:
            print("Lobby doesn't exist anymore\n")
            break
        data = r.json()
        for message in data["messages"]:
            print("-> " + message)
        time.sleep(2)

def chat(lobby_id, secret):
    threading.Thread(target=fetch_messages, args=(lobby_id, secret)).start()
    print("Type messages and press enter, you will start seeing messages when someone joins the lobby")
    while True:
        message = input()
        r = requests.post(hostname + "/api/send_message/" + lobby_id, data={"secret": secret, "message": message})
        if r.status_code != 200:
            break

def create_new_lobby():
    r = requests.get(hostname + "/api/create_lobby")
    data = r.json()
    lobby_id = str(data["id"])
    print("Created lobby with id " + lobby_id)
    chat(lobby_id, data["secret"])

def list_lobbies():
    r = requests.get(hostname + "/api/lobby_list")
    data = r.json()
    print("Available lobbies:")
    for lobby_id in data:
        print("  id: " + str(lobby_id))
    print()

def connect_to_lobby():
    lobby_id = input("Insert lobby id > ")
    r = requests.get(hostname + "/api/join_lobby/" + lobby_id)
    if r.status_code != 200:
        print("Lobby doesn't exist anymore")
        return
    data = r.json()
    secret = data["secret"]
    chat(lobby_id, secret)

while True:
    print("[0] create a new lobby\n[1] list lobbies\n[2] connect to lobby\n[3] exit\n")
    choice = input("> ")
    if choice == "0":
        create_new_lobby()
    elif choice == "1":
        list_lobbies()
    elif choice == "2":
        connect_to_lobby()
    elif choice == "3":
        break
    else:
        continue
