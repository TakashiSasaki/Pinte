import json

if __name__ == "__main__":
    print("GoogleOauth.py")
    file_native = open("google-oauth-native-application.json")
    dir_native = json.load(file_native)["installed"]
    for x in dir_native:
        print(x, dir_native[x])

    file_web = open("google-oauth-web-application.json")
    dir_web = json.load(file_web)["web"]
    for x in dir_web:
        print(x, dir_web[x])
