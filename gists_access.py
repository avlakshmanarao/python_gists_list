from github import Github
import os
from pprint import pprint
import datetime
import argparse
from tinydb import TinyDB, Query

def get_gists(token, username, timestamp):
    g1 = Github(token)
    try:
        for gst in g1.get_user(login=username).get_gists().reversed:
           pprint (gst.id + " :" + gst.description)
        saveLastAccessTime(username, timestamp)
    except Exception as err:
        pprint("Github user doesn't exists: "+username)


def get_gists_since_lastaccess(token, username, timestamp):
    g1 = Github(token)
    lastAccess=fetchLastAccessTime(username)
    if len(lastAccess) > 0 :
        lastAccessTime=lastAccess[0].get('timestamp')
        try:
           gists_list=g1.get_user(login=username).get_gists(since=datetime.datetime.strptime(lastAccessTime, '%Y-%m-%d %H:%M:%S')).reversed

        except github.GithubException as err:
           pprint("Github user doesn't exists")

        if gists_list.totalCount>0 :
            for gst in gists_list:
                pprint (gst.id + " :" + gst.description)
            saveLastAccessTime(username, timestamp)
        else:
            pprint("No further gists added after last access timestamp: "+lastAccessTime+" for user: "+username)
    else:
        get_gists(token,username,timestamp)

def getDatabase():
    try:
        database = TinyDB("gitdb.json")
    except Exception as exception:
        raise DatabaseError("Open connection error", exception)
    return database

def saveLastAccessTime(user, timestamp):
    dbtable = getDatabase().table("gistaccess")
    record = Query()
    result=dbtable.search(record.user == user)
    if len(result) > 0 :
        dbtable.update({"timestamp":timestamp}, record.user == user)
    else:
        dbtable.insert({"user":user, "timestamp":timestamp})
    getDatabase().close()

def fetchLastAccessTime(user):
    dbtable = getDatabase().table("gistaccess")
    record = Query()
    result=dbtable.search(record.user == user)
    getDatabase().close()
    return result



def main() :
    print(">>> Running.. to list gists for user:", os.getenv('username'))
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    parser = argparse.ArgumentParser(description='GITHUB_USER')
    parser.add_argument('--token', default=os.environ.get('GITHUB_TOKEN'))
    parser.add_argument('--username', required=True)
    parser.add_argument("-a", "--all", help="fetch all public gists belongs to user",
                    action="store_true")

    args = parser.parse_args()
    if not args.token:
         exit(parser.print_usage())
    if args.all:
        get_gists(args.token, args.username, now)
    else:
       get_gists_since_lastaccess(args.token, args.username, now)



if __name__ == "__main__":
    main()
