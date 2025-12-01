import psycopg2
import requiredFunctions

#Connect to DB -- PUT DB HERE
db = ""
usr = ""
login = ""

#Set up and validate connection
try:
    connection = psycopg2.connect(dbname=db, user=usr, password=login)
except:
    print("Invalid Connection")
    exit()

#Cursor for database operations
cur = connection.cursor()

def mainLoop():

    while True:
        selection = input("Please Select Login type: 1 - member, 2 - trainer, 3 - admin, 4 - register member or exit: ")
        

        if (selection == "1"):
            id = int(input("Please enter your id: "))
            cur.execute("""SELECT EXISTS (
                        SELECT * FROM Members
                        where member_id = %s)
                        """,(id,))
            if (cur.fetchall()[0][0]):
                print("Logged in as Member: ",id)
                memberMenu(id)
            else:
                print("User Not Found")
        elif(selection == "2"):
            id = int(input("Please enter your id: "))
            cur.execute("""SELECT EXISTS (
                        SELECT * FROM Trainer
                        where trainer_id = %s)
                        """,(id,))
            if (cur.fetchall()[0][0]):
                print("Logged in as Trainer: ",id)
                trainerMenu(id)
            else:
                print("User Not Found")
        elif(selection == "3"):
            id = int(input("Please enter your id: "))
            cur.execute("""
                        SELECT EXISTS (
                        SELECT * FROM Admins
                        where admin_id = %s)""",(id,))
            if (cur.fetchall()[0][0]):
                print("Logged in as Admin: ",id)
                adminMenu()
            else:
                print("User Not Found")
        elif(selection == "4"):
            addMember()
        elif(selection == "exit"):
            break

def addMember():
    #Execute and commit insert command, rolling back in case of failure
    name = input("Name: ") 
    email = input("Email: ")
    birth = input("Birthday: ")
    gender = input("Gender: ")
    phoneContact = input("Contact (phone): ")

    try:
        cur.execute("INSERT INTO Members (name, email, birthday, gender, contact) VALUES (%s, %s, %s, %s, %s)", (name, email, birth, gender, phoneContact))
        connection.commit()
    except:
        connection.rollback()
        print("Member Could Not Be Added")

def memberMenu(memberId):

    
    while True:
        selection = input("Please Select Option: 1 - View Dashboard 2 - Join Group Lesson  3 - Join Private Lesson or logout: ")

        try:
            if (selection == "1"):
                requiredFunctions.memberDashboard(cur,connection,memberId)
            elif(selection == "2"):
                requiredFunctions.memberJoinGroup(cur,connection,memberId)
            elif(selection == "3"):
                requiredFunctions.memberBookPrivate(cur,connection,memberId)
            elif(selection == "logout"):
                return  
        except:
            connection.rollback()
            print("Invalid Input")

def trainerMenu(trainerId):
    while True:
        selection = input("Please Select Option: 1 - View Classes 2 - Member Lookup or logout: ")

        try:
            if (selection == "1"):
                requiredFunctions.trainerViewClasses(cur,connection,trainerId)
            elif(selection == "2"):
                requiredFunctions.trainerLookupMember(cur,connection,trainerId)
            elif(selection == "logout"):
                return
        except:
            connection.rollback()
            print("Invalid Input")

def adminMenu():
    while True:
        selection = input("Please Select Option: 1 - Assign Room 2 - Create Class or logout: ")

        try:
            if (selection == "1"):
                requiredFunctions.adminAssignRoom(cur,connection)
            elif(selection == "2"):
                requiredFunctions.adminMakeClass(cur,connection)
            elif(selection == "logout"):
                return
        except:
            connection.rollback()
            print("Invalid Input")


mainLoop()
