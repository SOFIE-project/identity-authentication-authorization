import requests
import os
import argparse

def get_resource(resource, token):
    grant_type = {'access_token': token}
    response  = requests.post(resource, data = grant_type).text
    print("<---------")
    print ("Received response " + response)
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--resource', type=str, help="The URL of the resource")
    parser.add_argument('-t', '--token', type=str, help="The access token")
    if (args.resource and args.token):
        get_resource(args.resource, args.token)

    

if __name__ == '__main__':
    main()