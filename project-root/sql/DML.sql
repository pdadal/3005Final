INSERT INTO Members (name, email, birthday, gender, contact) VALUES
                ('John Doe', 'john.doe@example.com', '2000-09-01', 'Male', '613-555-1234'),
                ('Jane Smith', 'jane.smith@example.com', '2001-03-02', 'Female', '613-555-1982'),
				('Robert Ran', 'robran@example.com', '2001-10-12', 'Male', '313-555-1111'),
				('William Kennedy', 'will.kennedy3@example.com', '1998-01-08', 'Male', '613-555-2004'),
                ('Thomas Beam', 'thomas.beam@example.com', '2025-03-12', 'Male', '613-555-1200');
    
INSERT INTO Goals (member_id, goal_title, start_date, end_date) VALUES
                (1, 'Lose 10 lbs', 'Today', NULL),
                (1, 'Gain Muscle', '2023-09-01', 'Today'),
                (1, '50 Pushups', '2023-09-02', NULL),
				(2, 'Bench 175 lbs', '2022-06-22', '2023-06-22'),
				(3, 'Lose 5 lbs', '2022-07-17', NULL),
				(3, 'Reach 150 lbs', '2022-11-18', NULL),
				(4, 'Bench 200 lbs', '2024-01-01', '2024-09-28');
    
INSERT INTO Metrics (member_id, date, height, heart_rate, weight) VALUES
                (1, 'Today', 182, 100, 147),
                (1, '2025-11-01', 181, 95, 155),
				(1, '2025-10-01', 181, 110, 162),
				(1, '2025-09-01', 180, 93, 160),
				(2,'2023-12-28', 175, 110, 180),
				(3,'2023-05-20', 183, 88, 145),
				(3,'2022-12-28', 176, 120, 130),
				(4,'2024-09-01', 177, 90, 220);
    
INSERT INTO Trainer (name) VALUES
                ('Buffy Jump'),
                ('Rocky Balboa'),
				('Louis Liff');

INSERT INTO Admins (name) VALUES
                ('John Admin'),
                ('Joe Admin'),
				('Ron Admin');
    
INSERT INTO AvailibilityTimeslots (trainer_id, slot, occupied) VALUES
                (1, 'Fri-Morning', True),
                (1, 'Fri-Afternoon', True),
                (1, 'Fri-Night', False),
				
				(2, 'Mon-Night', True),
				(2, 'Tues-Night', True),
				(2, 'Wed-Night', False),
				
				(3, 'Wed-Morning', True),
				(3, 'Thur-Morning', True),
				(3, 'Tues-Morning', False);
    
INSERT INTO Rooms (location) VALUES
                ('100 Minto'),
                ('200 St. Pats'),
				
				('210 Weights Center'),
                ('1234 Main Place');

INSERT INTO GroupBookings (timeslot_id, room_id, capacity) VALUES
                (1, 1, 1),
				
				(4, 3, 5),
				(5, 2, 4);
    
INSERT INTO PrivateBookings (member_id, room_id, timeslot_id) VALUES
                (1, 1, 2),
				
				(1, 2, 7),
				(3, 3, 8);


INSERT INTO Registrations (member_id, booking_id) VALUES
				(1, 1),
				(2, 2),
				(2, 3),
				(3, 2),
				(3, 3),
				(4, 2);