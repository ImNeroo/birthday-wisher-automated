import pandas
import smtplib
import os
from dotenv import load_dotenv
import datetime as dt
import random

load_dotenv("datamine.env")
my_email = os.getenv("MY_EMAIL")
password = os.getenv("PASSWORD")
SMTP = os.getenv("SMTP")
PORT = int(os.getenv("PORT"))


now = dt.datetime.now()
now_month = now.month
now_day = now.day
now_year = now.year

data = pandas.read_csv("birthdays.csv")
new_dict = data.to_dict(orient="records")
file_path = f"letter_templates/letter_{random.randint(1,3)}.txt"
with open(file_path) as letter:
    new_letter = letter.read()
for item in new_dict:
    if item["month"] == now_month and item["day"] == now_day:
        with open("letter_templates/new_letter.txt", mode="w") as file:
            file.write(new_letter.replace("[NAME]", item["name"]))
        with open("letter_templates/new_letter.txt") as letter:
            letter_to_send = letter.read()
        with smtplib.SMTP(SMTP, port=PORT) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=item["email"],
                msg=f"Subject:Happy Birthday!!\n\n{letter_to_send}"
            )





