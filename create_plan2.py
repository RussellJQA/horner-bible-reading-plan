import calendar
import csv
import datetime
import re
import string
from dataclasses import dataclass

from prettytable import PrettyTable


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
    day: int | None


def get_plan_readings(
    start_date: datetime.date,
    end_date: datetime.date,
    chapter_counts: dict[str, str],
    book_groups: list[BookGroup],
):

    for book_group in book_groups:
        book_group.set_readings(chapter_counts)
    
    group_names_with_num_readings = {book_group.group_name : len(book_group.readings) for book_group in book_groups}
    print(f"Groups, each with its number of distinct readings: {group_names_with_num_readings}\n")

    column_names: list[str] = ["Date"] + [book_group.group_name for book_group in book_groups]
    table = PrettyTable(column_names)

    # plan_readings_raw = []
    previous_year_and_month: str | None = None
    current_year_and_month: str | None = None
    day: int | None = None
    months_with_start_days: list[MonthWithStartDay] = []


    number_of_days_in_plan = (end_date - start_date).days + 1
    date: datetime.date = start_date
    for day in range(number_of_days_in_plan):
        days_readings: list[str] = [str(date)]
        current_year_and_month = date.strftime("%B %Y")
        if current_year_and_month != previous_year_and_month:
            months_with_start_days += [MonthWithStartDay(current_year_and_month, day)]
        for book_group in book_groups:
            days_readings.append(book_group.readings[book_group.reading_index])
            book_group.increment_reading_index()
        table.add_row(days_readings)

        date += datetime.timedelta(days=1)
        previous_year_and_month = current_year_and_month
        # plan_readings_raw.append(days_readings)

    months_with_start_days += [MonthWithStartDay(current_year_and_month, day)]
    # print(f"{current_year_and_month} starts on day {day}")

    # print(months_with_start_days)
    for month_with_start_day in months_with_start_days:
        print(month_with_start_day)

    # print(plan_readings_raw)
    html_string = table.get_html_string()
    # print(html_string)



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

    abbreviations: dict[str, str] = {}
    chapter_counts: dict[str, str] = {}
    with open("bible_book_info.csv", "r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            abbreviations[row["book"]] = row["abbreviation"]
            chapter_counts[row["book"]] = row["chapters"]

    start_date = datetime.date(2023, 1, 1)
    end_date = datetime.date(2023, 12, 31)
    date_range: str = f"{start_date.strftime('%Y%m%d')}-{end_date.strftime('%Y%m%d')}"

    # plan_readings_raw: list[dict[str, str]] = get_plan_readings(start_date, end_date, chapter_counts, book_groups)
    get_plan_readings(start_date, end_date, chapter_counts, book_groups)
   

if __name__ == "__main__":
    main()
