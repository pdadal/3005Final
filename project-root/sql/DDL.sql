----------------------------------------------
-- Starting Data
-------------------------------------------------

DROP VIEW IF EXISTS classTrainerNames;

DROP TRIGGER IF EXISTS occupyGroup ON GroupBookings;
DROP TRIGGER IF EXISTS occupyPrivate ON PrivateBookings;
DROP FUNCTION IF EXISTS occupyTimeSlot();

DROP INDEX IF EXISTS goalIndex;

DROP TABLE IF EXISTS Registrations;
DROP TABLE IF EXISTS GroupBookings;
DROP TABLE IF EXISTS PrivateBookings;
DROP TABLE IF EXISTS AvailibilityTimeslots;
DROP TABLE IF EXISTS Rooms;
DROP TABLE IF EXISTS Metrics;
DROP TABLE IF EXISTS Goals;
DROP TABLE IF EXISTS Trainer;
DROP TABLE IF EXISTS Members;
DROP TABLE IF EXISTS Admins;

------------------------------------------------------
-- Table Creation
------------------------------------------------------

CREATE TABLE Members (
        member_id  INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        name    VARCHAR(255)    NOT NULL,
        email   VARCHAR(255)    UNIQUE NOT NULL,
        birthday    DATE    NOT NULL,
        gender  VARCHAR(255)    NOT NULL,
        contact VARCHAR(255)    NOT NULL
        );

CREATE TABLE Trainer (
                trainer_id  INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                name VARCHAR(255) NOT NULL
                );

CREATE TABLE Admins (
        admin_id  INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        name    VARCHAR(255)    NOT NULL
        );
    
CREATE TABLE Goals (
		goal_id  INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- New
        member_id INT NOT NULL,
        goal_title VARCHAR(255),
        start_date DATE NOT NULL,
        end_date DATE,
        FOREIGN KEY (member_id) REFERENCES Members(member_id)
        );

CREATE TABLE Metrics ( -- Note this previously had metricId as a priamry key
		metric_id  INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- New
        member_id INT   NOT NULL,
        date    DATE    NOT NULL,
        height  FLOAT,
        heart_rate  INT,
        weight  FLOAT,
        FOREIGN KEY (member_id) REFERENCES Members(member_id)
        );

CREATE TABLE Rooms (
        room_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        location VARCHAR(255) UNIQUE
        );

CREATE TABLE AvailibilityTimeslots (
        timeslot_id  INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        trainer_id  INT NOT NULL,
        slot VARCHAR(255) NOT NULL,
        occupied BOOLEAN NOT NULL,
        FOREIGN KEY (trainer_id) REFERENCES Trainer (trainer_id)
        );

CREATE TABLE PrivateBookings (
		booking_id  INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- New
        member_id INT NOT NULL,
        room_id INT NOT NULL,
        timeslot_id INT NOT NULL,--? Maybe table for this?
        FOREIGN KEY (member_id) REFERENCES Members(member_id),
        FOREIGN KEY (room_id) REFERENCES Rooms(room_id),
        FOREIGN KEY (timeslot_id) REFERENCES AvailibilityTimeslots(timeslot_id)
        );

CREATE TABLE GroupBookings (
        booking_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        timeslot_id INT NOT NULL,
        room_id INT NOT NULL,
        capacity INT NOT NULL,
        FOREIGN KEY (timeslot_id) REFERENCES AvailibilityTimeslots(timeslot_id),
        FOREIGN KEY (room_id) REFERENCES Rooms(room_id)
        );

CREATE TABLE Registrations (
        member_id INT NOT NULL,
        booking_id INT NOT NULL,
        FOREIGN KEY (member_id) REFERENCES Members(member_id),
        FOREIGN KEY (booking_id) REFERENCES GroupBookings(booking_id)
        );


------------------------------------------------------
-- Index/Triggers/View Creation
------------------------------------------------------
CREATE INDEX goalIndex on Goals(member_id, goal_title, start_date, end_date);

CREATE FUNCTION occupyTimeSlot()
returns TRIGGER
language plpgsql
AS
$$
begin
	UPDATE AvailibilityTimeslots 
	SET occupied = True 
	WHERE timeslot_id = NEW.timeslot_id;
	RETURN NEW;
end;
$$;

CREATE TRIGGER occupyGroup
BEFORE INSERT
ON GroupBookings
FOR EACH ROW
EXECUTE PROCEDURE occupyTimeSlot();

CREATE TRIGGER occupyPrivate
BEFORE INSERT
ON PrivateBookings
FOR EACH ROW
EXECUTE PROCEDURE occupyTimeSlot();

CREATE VIEW classTrainerNames AS
SELECT g.booking_id, t.name, t.trainer_id, a.slot
FROM GroupBookings g
JOIN AvailibilityTimeslots a ON g.timeslot_id = a.timeslot_id
JOIN Trainer t ON a.trainer_id = t.trainer_id;