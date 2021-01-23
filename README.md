# python_gists_list
Python script to list down all latest gists since last access time for specified user

I. Pre-Requisits

      1. Have Linux VM with Ubuntu or any other equivalent Linux flavour
      
      2. python3 will be automatically installed with latest version of Linux OS.
            2a) check python3 --version  
            2b) if it doesn't exists, get it installed from https://www.python.org/downloads/source/
            
      3.  install pip, Tiny DB and PyGithub API packages
             sudo apt install python3-pip
             pip3 install tinydb
             pip3 install PyGithub requests

      4. Generate personal access token in github account  from settings --> developer settings.   Copy the token string


II. How to run?

      1.  Download this project into your Linux VM and extract it to local folder or simply run git clone cmd
      2.  python3 gists_access.py --token <<GITHUB_TOKEN>> --username <<GITHUB_USER>>
            <<GITHUB_TOKEN>>  - personal access token copied earlier
            <<GITHUB_USER>>   - Any github user id who published their public gists at github.com




III. How it works? - design consideration

      1.  Passing GITHUB_TOKEN is not mandatory initially.. but after running few times Github blocks access due to limitations imposed on unauthenticated user.  Therefore I made it mandatory for supplying authenticated GITHUB_TOKEN

      2.  Program will generate gitdb.json in the same directory by TinyDB to persist last access datetime stamp for every user.

      3.  First when main program calls function  "get_gists_since_lastaccess", following thing will happen
          3a) Program try to fetch last access time stamp of github user from local DB
          3b) If local record doesn't exists, it will run to fetch all gists posted by user and saves timestamp to gitdb.json
          3c) For all subsequent runs, program will fetch all gists since last successful saved timestamp and updates existing timestamp.  
          3d) If no further gists posted by user since last time, program displays message.

          Note: Ensure you pass valid github username, otherwise, it will end-up with error "Github user doesn't exists"




IV. Additional Feature - Fetch all gists belongs to user at any point of time

      1.  Simply pass -a to the command
          python3 gists_access.py --token <<GITHUB_TOKEN>> --username <<GITHUB_USER>> -a

          This also will update  time stamp to existing user.  For new users, it creates new entry in localDB.
