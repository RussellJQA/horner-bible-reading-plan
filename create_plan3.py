import calendar
import csv
import datetime
import re
import string
from dataclasses import dataclass

from prettytable import PrettyTable

def get_chapter_counts() -> dict[str, str]:

    chapter_counts: dict[str, str] = {}
    with open("bible_book_info.csv", "r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            chapter_counts[row["book"]] = row["chapters"]

    return chapter_counts


class BookGroup:

    # Set by constructor
    group_name: str
    book_list: list[str]
    reading_index: int

    readings: list[str]

    def __init__(self, group_name: str, book_list: list[str], reading_index: int = 0):
        self.group_name = group_name
        self.book_list = book_list
        self.reading_index = reading_index

    def set_readings(self, chapter_counts: dict[str, str]):
        self.readings = []
        for book in self.book_list:
            for chapter in range(1, int(chapter_counts[book]) + 1):
                self.readings.append(f"{book} {chapter}")

    def increment_reading_index(self):
        if self.reading_index < len(self.readings) - 1:
            self.reading_index += 1
        else:
            self.reading_index = 0

@dataclass
class MonthWithStartDay:
    month_name: str | None
    day: int

@dataclass
class ReadingsInfo:
    page_heading: str
    column_names: list[str]
    plan_readings: list[list[str]] 

def get_overall_readings_info(
    start_date: datetime.date,
    end_date: datetime.date,
    book_groups: list[BookGroup],
) -> ReadingsInfo:

    page_heading: str = f"Bible Reading Plan for: {start_date} to {end_date}"

    column_names: list[str] = ["Date"] + [book_group.group_name for book_group in book_groups]
    # print(column_names)

    chapter_counts: dict[str, str] = get_chapter_counts()
    for book_group in book_groups:
        book_group.set_readings(chapter_counts)
    
    # group_names_with_num_readings = {book_group.group_name : len(book_group.readings) for book_group in book_groups}
    # print(f"Groups, each with its number of distinct readings: {group_names_with_num_readings}\n")

    plan_readings: list[list[str]] = []

    number_of_days_in_plan = (end_date - start_date).days + 1
    date: datetime.date = start_date
    for day in range(number_of_days_in_plan):
        days_readings: list[str] = [str(date)]
        for book_group in book_groups:
            days_readings.append(book_group.readings[book_group.reading_index])
            book_group.increment_reading_index()

        date += datetime.timedelta(days=1)
        plan_readings.append(days_readings)

    overall_readings_info =  ReadingsInfo(page_heading, column_names, plan_readings)

    return overall_readings_info


def main():

    book_groups: list[BookGroup] = [
        BookGroup("Gospels", ["Matthew", "Mark", "Luke", "John"]),
        BookGroup("Pentateuch", ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy"]),
        BookGroup(
            "Epistles1",
            [
                "Romans",
                "1 Corinthians",
                "2 Corinthians",
                "Galatians",
                "Ephesians",
                "Philippians",
                "Colossians",
                "Hebrews",
            ],
        ),
        BookGroup(
            "Epistles2",
            [
                "1 Thessalonians",
                "2 Thessalonians",
                "1 Timothy",
                "2 Timothy",
                "Titus",
                "Philemon",
                "James",
                "1 Peter",
                "2 Peter",
                "1 John",
                "2 John",
                "3 John",
                "Jude",
                "Revelation",
            ],
        ),
        BookGroup("Wisdom", ["Job", "Ecclesiastes", "Song of Songs"]),
        BookGroup("Psalms", ["Psalms"]),
        BookGroup("Proverbs", ["Proverbs"]),
        BookGroup(
            "History",
            [
                "Joshua",
                "Judges",
                "Ruth",
                "1 Samuel",
                "2 Samuel",
                "1 Kings",
                "2 Kings",
                "1 Chronicles",
                "2 Chronicles",
                "Ezra",
                "Nehemiah",
                "Esther",
            ],
        ),
        BookGroup(
            "Prophets",
            [
                "Isaiah",
                "Jeremiah",
                "Lamentations",
                "Ezekiel",
                "Daniel",
                "Hosea",
                "Joel",
                "Amos",
                "Obadiah",
                "Jonah",
                "Micah",
                "Nahum",
                "Habakkuk",
                "Zephaniah",
                "Haggai",
                "Zechariah",
                "Malachi",
            ],
        ),
        BookGroup("Acts", ["Acts"]),
    ]

    start_date = datetime.date(2023, 1, 1)
    end_date = datetime.date(2023, 12, 31)
    date_range: str = f"{start_date.strftime('%Y%m%d')}-{end_date.strftime('%Y%m%d')}"
    overall_readings_info: ReadingsInfo = get_overall_readings_info(start_date, end_date, book_groups)
    # print(overall_readings_info.page_heading)
    # for reading in overall_readings_info.plan_readings:
    #     print(reading)

    months_of_readings: list[ReadingsInfo] = []

    previous_year_and_month: str | None = None
    current_year_and_month: str | None = None
    day: int | None = None
    months_with_start_days: list[MonthWithStartDay] = []

    for day, reading in enumerate(overall_readings_info.plan_readings):
        current_year_and_month = reading[0][0:7]
        if current_year_and_month != previous_year_and_month:
            months_with_start_days += [MonthWithStartDay(current_year_and_month, day)]
        previous_year_and_month = current_year_and_month

    if day:
        months_with_start_days += [MonthWithStartDay(current_year_and_month, day + 1)]

    for index, month_with_start_day in enumerate(months_with_start_days[:-1]):
        end_day = months_with_start_days[index+1].day
        print(month_with_start_day.month_name, month_with_start_day.day, end_day)

if __name__ == "__main__":
    main()
