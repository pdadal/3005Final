#MEMBER FUNC 2 DISPLAY DASHBOARD
def memberDashboard(cur,connection,memberId):

    print()
    print("Member:")
    print()
    cur.execute("SELECT * FROM Members WHERE member_id = %s;", (memberId,))
    printTable(cur.description,cur.fetchall())

    print()
    print("Active Goals:")
    print()
    cur.execute("SELECT * FROM Goals WHERE member_id = %s AND end_date IS NULL;", (memberId,))
    printTable(cur.description,cur.fetchall())

    print()
    print("Last 3 Health Metrics:")
    print()
    cur.execute("SELECT * FROM Metrics WHERE member_id = %s ORDER BY date DESC LIMIT 3;", (memberId,))
    printTable(cur.description,cur.fetchall())

#MEMBER FUNC 3 BOOK PRIVATE LESSON
def memberBookPrivate(cur,connection,memberId):
    print("All Trainers/times")
    cur.execute("SELECT timeslot_id,trainer_id,slot FROM AvailibilityTimeslots WHERE occupied = False;")
    desc, availabilities = cur.description,cur.fetchall()
    validAvailibilies = set()
    for row in availabilities:
        validAvailibilies.add(row[0])

    printTable(desc,availabilities)

    timeslot = int(input("Please enter timeslot: "))

    rooms = list(getFreeRoomsAtTime(cur, connection, timeslot))
    
    if (timeslot not in getFreeTimeslots(cur, connection)) or len(rooms) < 0:
        print("No Rooms Availible for Booking")
        return

    
    
    cur.execute("INSERT INTO PrivateBookings (member_id, room_id, timeslot_id) VALUES (%s, %s, %s);", (memberId, rooms[0], timeslot))
    ##occupyTimeslot(cur, connection, timeslot) # Replaced with trigger

    connection.commit()

#MEMBER FUNC 3 JOIN PUBLIC LESSON
def memberJoinGroup(cur,connection,memberId):
    print("FULL CLASSLIST:")
    cur.execute("""SELECT * FROM classTrainerNames;""")
    des,result = cur.description,cur.fetchall()
    printTable(des,result) 

    print("All Group Classes You Are Eligible for Registration:")
    #cur.execute("SELECT * FROM GroupBookings;")
    cur.execute("""SELECT * FROM GroupBookings g
    WHERE NOT EXISTS (
        SELECT 1 FROM Registrations r
        WHERE r.member_id = %s AND r.booking_id = g.booking_id
    );""",(memberId,))

    des,result = cur.description,cur.fetchall()
    
    printTable(des,result)

    classIds = set()
    for row in result:
        classIds.add(row[0])
    ##print(classIds)


    response = input("Which Class Would You Like To Join?: ")

    if (not int(response) in classIds):
        print("Invalid Class or Already Registered")
        return

    #Get Class Capacity:
    cur.execute("SELECT capacity FROM GroupBookings WHERE booking_id = %s",(int(response),))
    capacity = cur.fetchall()[0][0]
    print("Retrieved Capacity: ",capacity)
    cur.execute("SELECT count(member_id) FROM Registrations WHERE booking_id = %s", (int(response),)) #Safety check int?
    currentMembers = cur.fetchall()[0][0]
    print("currentMembers: ",currentMembers)

    #If class is not at max capacity:
    if (currentMembers < capacity):
        cur.execute("INSERT INTO Registrations (member_id, booking_id) Values (%s, %s)", (memberId, int(response))) #Safety check int?
        connection.commit()
    else:
        print("Class is Full")

#TRAINER FUNC 1 VIEW UPCOMING CLASSES
def trainerViewClasses(cur,connection,trainerId):
    #Group Classes
    cur.execute("""
    Select g.* from GroupBookings g
    WHERE EXISTS (
        SELECT 1
        FROM AvailibilityTimeslots a
        WHERE
        g.timeslot_id = a.timeslot_id AND a.trainer_id = %s
    );  
    """,(trainerId,))
    print("Group Classes")
    #print(cur.fetchall())
    printTable(cur.description,cur.fetchall())
    print()

    #Private Classes
    cur.execute("""
    Select p.* from PrivateBookings p
    WHERE EXISTS (
        SELECT 1
        FROM AvailibilityTimeslots a
        WHERE
        p.timeslot_id = a.timeslot_id AND a.trainer_id = %s
    );
    """,(trainerId,))
    print("Private Lessons")
    #print(cur.fetchall())
    printTable(cur.description,cur.fetchall())
    print()

#TRAINER FUNC 2 LOOK UP MEMBER
def trainerLookupMember(cur,connection,trainerId):
    #Get Member IDs
    cur.execute("""
    Select p.member_id from PrivateBookings p
    WHERE EXISTS (
        SELECT 1
        FROM AvailibilityTimeslots a
        WHERE
        p.timeslot_id = a.timeslot_id AND a.trainer_id = %s
    )
    UNION
    select r.member_id FROM Registrations r
    JOIN GroupBookings g ON r.booking_id = g.booking_id
    JOIN AvailibilityTimeslots a ON g.timeslot_id = a.timeslot_id
    WHERE a.trainer_id = %s
    ; 
    """,(trainerId,trainerId))
    ids = cur.fetchall()
    print(ids)
    idSet = set()

    for i in ids:
        idSet.add(i[0])
    
    chosenMember = input("Please choose MemberId you wish to lookup: ")

    print(idSet)
    print(int(chosenMember) in idSet)

    if (not int(chosenMember) in idSet):
        print("Unauthorised to access Member")
        return
    
    print("Member's active Goals:")
    cur.execute("SELECT * FROM Goals WHERE member_id = %s AND end_date IS NULL;", (int(chosenMember),))
    print(cur.fetchall())

    print("Member's Last Health Metrics:")
    cur.execute("SELECT * FROM Metrics WHERE member_id = %s ORDER BY date DESC LIMIT 1;", (int(chosenMember),))
    print(cur.fetchall())

#ADMIN FUNC 1 ASSIGN ROOMS TO CLASSES
def adminAssignRoom(cur,connection):

    while True:
        choice = input("Would you like to assign a room to a 'private' or 'group' class?: ")

        if (choice == "private" or choice == "group"):
            break
    

    #Group
    if (choice == "group"):
        #TODO: List Classes
        lesson = int(input("Please Enter Lesson Id: "))
        room = int(input("Please Enter Room Id: "))

        

        #Get Current Timeslot
        cur.execute("""
        SELECT timeslot_id FROM GroupBookings
        WHERE booking_id = %s;
        """, (lesson,))
        response = cur.fetchall()[0][0]
        time = response

        #Do Verification on new room with current timeslot
        print("Free Rooms at timeslot: ",getFreeRoomsAtTime(cur, connection, time))

        if (not room in getFreeRoomsAtTime(cur, connection, time)):
            print("Room Unavailible at time")
            return

        #Update Room with new slot
        cur.execute(""" 
        UPDATE GroupBookings SET  room_id = %s WHERE booking_id = %s;
        """, (room, lesson))
        #Free old timeslot
        ##freeTimeslot(time)
        #Occupy Used Timeslot
        ##occupyTimeslot()
        connection.commit()

#ADMIN FUNC 2 ADD CLASSES, ASSIGN TRAINERS/ROOMS/TIMES?
def adminMakeClass(cur,connection): #TEST TO VERIFY
    time = int(input("Please Enter Timeslot Id: "))
    room = int(input("Please Enter Room Id: "))
    capacity = int(input("Please Enter capacity: "))

    #Do Verification Here...

    if (time not in getFreeTimeslots(cur, connection) or room not in getFreeRoomsAtTime(cur, connection, time)):
        print("Invalid TimeSlot / Room Combo")
        return

    cur.execute("""
    INSERT INTO GroupBookings (timeslot_id, room_id, capacity) VALUES
    (%s, %s, %s);
    """,(time, room, capacity))

    ##occupyTimeslot(cur, connection, time) # Replaced with trigger
    connection.commit()


#helpers
def getFreeTimeslots(cur,connection):
    ret = set()

    cur.execute("""
    SELECT timeslot_id FROM AvailibilityTimeslots 
    WHERE occupied = False;
    """)

    ids = cur.fetchall()

    for i in ids:
        ret.add(i[0])
    return(ret)

def getFreeRoomsAtTime(cur,connection,timeslotId): # VERIFY
    ret = set()

    #cur.execute("""
    #SELECT room_id from Rooms
    #EXCEPT
    #SELECT p.room_id from PrivateBookings p
    #JOIN AvailibilityTimeslots a ON a.timeslot_id = p.timeslot_id
    #WHERE a.slot = (
    #    SELECT slot from AvailibilityTimeslots 
    #    WHERE timeslot_id = %s
    #);
    #""", (timeslotId, ))
    
    cur.execute("""
        SELECT room_id from Rooms
        EXCEPT 
        (SELECT p.room_id from PrivateBookings p
        JOIN AvailibilityTimeslots a ON a.timeslot_id = p.timeslot_id
        WHERE a.timeslot_id = %s
        UNION
        SELECT g.room_id from GroupBookings g
        JOIN AvailibilityTimeslots a ON a.timeslot_id = g.timeslot_id
        WHERE a.timeslot_id = %s)
        ;
    """, (timeslotId, timeslotId))

    ids = cur.fetchall()

    for i in ids:
        ret.add(i[0])
    return(ret)

#VERIFY THESE Two
def occupyTimeslot(cur,connection,timeslotId):
    cur.execute("""
                UPDATE AvailibilityTimeslots SET occupied = True WHERE timeslot_id = %s;""",(timeslotId,))
    connection.commit()

def freeTimeslot(cur,connection,timeslotId):
    cur.execute("""
                UPDATE AvailibilityTimeslots SET occupied = False WHERE timeslot_id = %s;""",(timeslotId,))
    connection.commit()

def printTable(headers,data):
    for label in headers:
        print(label[0],end="\t")
    print()
    for row in data:
        for field in row:
            print(field,end="\t")
        print()
