-- Keep a log of any SQL queries you execute as you solve the mystery.
-- I think we can start with the crime scene reports and see if they're is anything suspicious
SELECT description FROM crime_scene_reports
WHERE year = 2024
AND month = 7
AND day = 28
AND street = 'Humphrey Street';
-- Now I will see the interviews with the three witnesses
SELECT transcript FROM interviews
WHERE year = 2024
AND month = 7
AND day = 28;
-- The interview was usefull and has three clues the camera footage, the atm and the flight
-- Next step is to find infos here
-- First we check the security camera
SELECT activity, license_plate FROM bakery_security_logs
WHERE year = 2024
AND month = 7
AND day = 28
AND hour = 10
AND minute BETWEEN 15 AND 25;

-- Now we see the atm
SELECT account_number, transaction_type, amount FROM atm_transactions
WHERE year = 2024
AND month = 7
AND day = 28
AND atm_location = 'Leggett Street';

-- Now we see the phone call

SELECT caller,receiver FROM phone_calls
WHERE year = 2024
AND month = 7
AND day = 28
AND duration < 60;

-- We are getting close now we see the flight and the bookings

SELECT id, origin_airport_id, destination_airport_id, hour, minute FROM flights
WHERE year = 2024
AND month = 7
AND day = 29 ORDER BY hour ASC, minute ASC;

-- We know the flight id

SELECT passport_number FROM passengers WHERE flight_id = 36;

-- now we have all the necessary inf to know the thief

SELECT DISTINCT id, name FROM people JOIN bank_accounts ON person_id = id
WHERE phone_number IN (SELECT caller FROM phone_calls
                        WHERE year = 2024
                        AND month = 7
                        AND day = 28
                        AND duration < 60)
AND license_plate IN (SELECT license_plate FROM bakery_security_logs
                        WHERE year = 2024
                        AND month = 7
                        AND day = 28
                        AND hour = 10
                        AND minute BETWEEN 15 AND 25)
AND account_number IN (SELECT account_number FROM atm_transactions
        WHERE year = 2024
        AND month = 7
        AND day = 28
        AND atm_location = 'Leggett Street'
        AND transaction_type = 'withdraw')
AND passport_number IN (
    SELECT passport_number FROM passengers
    WHERE flight_id = 36
);

-- OK the thief is Bruce
-- We need the find the destination

SELECT city, full_name FROM airports WHERE id = 4;


--Find the number of the thief
SELECT phone_number FROM people WHERE id = 686048;

-- Find the accomplice through the phone_number

SELECT name FROM people WHERE phone_number = '(375) 555-8161';
