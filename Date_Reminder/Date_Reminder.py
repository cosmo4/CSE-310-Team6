import datetime
from send_email import send_email

test_day = int(input("What day is your next test? "))
test_month = int(input("What month is your next test? "))
email = input("What is your email? ")
current_time = datetime.datetime.now()
next_test =  datetime.datetime(2024, test_month, test_day)
reminder_day = datetime.datetime(2024, test_month, (test_day - 2), 11)

print("Current Time: ", current_time)
print("Next Test: ", next_test)
print("Day for Reminder: ", reminder_day)

if (current_time >= reminder_day):
    send_email(email)