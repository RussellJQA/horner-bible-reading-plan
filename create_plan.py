import calendar
import csv
import datetime
import re
import string

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


def get_plan_readings(
    start_date: datetime.date,
    end_date: datetime.date,
    chapter_counts: dict[str, str],
    book_groups: list[BookGroup],
) -> list[dict[str, str]]:

    print("\nGroup names, each with its number of distinct readings")
    for book_group in book_groups:
        book_group.set_readings(chapter_counts)
        print(f"\t{book_group.group_name}: {len(book_group.readings)}")

    plan_readings_raw = []
    number_of_days_in_plan = (end_date - start_date).days + 1
    date: datetime.date = start_date
    for day in range(number_of_days_in_plan):
        days_readings: dict[str, str] = {"Date": str(date)}
        for book_group in book_groups:
            days_readings[book_group.group_name] = book_group.readings[book_group.reading_index]
            book_group.increment_reading_index()
        date += datetime.timedelta(days=1)
        plan_readings_raw.append(days_readings)

    return plan_readings_raw


def get_formatted_date(date: datetime.date) -> str:
    day_of_week = str(date.strftime("%a"))
    day_of_week = "L.D." if (day_of_week == "Sun") else day_of_week
    return (
        f"{day_of_week} {str(date.strftime('%m/%e')).removeprefix('0').replace(' ', '')}"  # Remove/replace 0-padding
    )


def get_formatted_reading(reading: str, abbreviations: dict[str, str], chapter_counts: dict[str, str]) -> str:
    pattern = re.compile(r"(.*) (\d+$)")
    matches = pattern.match(reading)
    if matches:
        book = matches.group(1)
        chapter = matches.group(2)
        if chapter_counts[book] == "1":  # if reading is for a 1-chapter book
            return book.replace(
                " ", ""
            )  # then replace the reading with just the unabbreviated book name (without blank spaces)
            # "2 John" -> "2John" and "3 John" -> "3John"
        else:
            return f"{abbreviations[book]} {chapter}"
    else:
        raise ValueError(
            f"The specified reading ('{reading}') doesn't contain a Bible book and chapter in the expected format."
        )


def get_plan_readings_formatted(
    plan_readings_raw: list[dict[str, str]],
    abbreviations: dict[str, str],
    chapter_counts: dict[str, str],
) -> list[dict[str, str]]:

    plan_readings_formatted: list[dict[str, str]] = []

    for days_readings in plan_readings_raw:
        days_readings_formatted: dict[str, str] = {}
        for key, value in days_readings.items():
            if key == "Date":
                date = datetime.date(int(value[0:4]), int(value[5:7]), int(value[8:10]))
                days_readings_formatted[key] = get_formatted_date(date)
            else:
                days_readings_formatted[key] = f"{get_formatted_reading(value, abbreviations, chapter_counts)}"
        plan_readings_formatted.append(days_readings_formatted)

    return plan_readings_formatted


def write_readings_to_csv(plan_readings: list[dict[str, str]], csv_file_prefix: str, date_range: str):
    column_headings = ",".join(plan_readings[0].keys())
    with open(f"{csv_file_prefix}-{date_range}.csv", "w", encoding="utf-8") as csv_file:
        csv_file.write(f"{column_headings}\n")
        for days_readings in plan_readings:
            column_data = ",".join(days_readings.values())
            csv_file.write(f"{column_data}\n")


def write_readings_to_html(plan_readings: list[dict[str, str]], csv_file_prefix: str, date_range: str):

    # Adapted from https://www.pythonforbeginners.com/basics/convert-csv-to-html-table-in-python
    # and https://www.geeksforgeeks.org/convert-csv-to-html-table-in-python/

    with open(f"{csv_file_prefix}-{date_range}.csv", "r", encoding="utf-8") as csv_file:

        data = csv_file.readlines()
        column_names = data[0].split(",")
        table = PrettyTable(column_names)

        for i in range(1, len(data)):
            table.add_row(data[i].split(","))
        html_string = table.get_html_string()

        with open(f"{csv_file_prefix}-{date_range}-table.html", "w", encoding="utf-8") as html_file:
            html_file.writelines(html_string)

        with open("horner-classic-formatted-template.html", "r", encoding="utf-8") as template_file:
            template_string = template_file.read()
        text_template = string.Template(template_string)

        # TODO: The code below is hard-coded to work only for a plan lasting from Jan. 1 thru Dec. 31 2023
        #   Make it work instead in the general case

        heading_and_table1 = f"    <h3>Horner Classic Bible Reading Plan - January 2023 </h3>\n{table[0:31].get_html_string()}"
        heading_and_table2 = f"    <h3>Horner Classic Bible Reading Plan - February 2023 </h3>\n{table[31:59].get_html_string()}"
        heading_and_table3 = f"    <h3>Horner Classic Bible Reading Plan - March 2023 </h3>\n{table[59:90].get_html_string()}"
        heading_and_table4 = f"    <h3>Horner Classic Bible Reading Plan - April 2023 </h3>\n{table[90:120].get_html_string()}"
        heading_and_table5 = f"    <h3>Horner Classic Bible Reading Plan - May 2023 </h3>\n{table[120:151].get_html_string()}"
        heading_and_table6 = f"    <h3>Horner Classic Bible Reading Plan - June 2023 </h3>\n{table[151:181].get_html_string()}"
        heading_and_table7 = f"    <h3>Horner Classic Bible Reading Plan - July 2023 </h3>\n{table[181:212].get_html_string()}"
        heading_and_table8 = f"    <h3>Horner Classic Bible Reading Plan - August 2023 </h3>\n{table[212:243].get_html_string()}"
        heading_and_table9 = f"    <h3>Horner Classic Bible Reading Plan - September 2023 </h3>\n{table[243:273].get_html_string()}"
        heading_and_table10 = f"    <h3>Horner Classic Bible Reading Plan - October 2023 </h3>\n{table[273:304].get_html_string()}"
        heading_and_table11 = f"    <h3>Horner Classic Bible Reading Plan - November 2023 </h3>\n{table[304:334].get_html_string()}"
        heading_and_table12 = f"    <h3>Horner Classic Bible Reading Plan - December 2023 </h3>\n{table[334:365].get_html_string()}"

        readings = text_template.substitute(
            heading_and_table1=heading_and_table1,
            heading_and_table2=heading_and_table2,
            heading_and_table3=heading_and_table3,
            heading_and_table4=heading_and_table4,
            heading_and_table5=heading_and_table5,
            heading_and_table6=heading_and_table6,
            heading_and_table7=heading_and_table7,
            heading_and_table8=heading_and_table8,
            heading_and_table9=heading_and_table9,
            heading_and_table10=heading_and_table10,
            heading_and_table11=heading_and_table11,
            heading_and_table12=heading_and_table12,
        )
        readings = readings.replace('<table>', '<table role="presentation">')
        with open("horner-classic-formatted-20230101-20231231.html", "w", encoding="utf-8") as html_file:
            html_file.writelines(readings)


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

    plan_readings_raw: list[dict[str, str]] = get_plan_readings(start_date, end_date, chapter_counts, book_groups)
    write_readings_to_csv(plan_readings_raw, "horner_classic", date_range)

    plan_readings_formatted: list[dict[str, str]] = get_plan_readings_formatted(
        plan_readings_raw, abbreviations, chapter_counts
    )
    write_readings_to_csv(plan_readings_formatted, "horner-classic-formatted", date_range)
    write_readings_to_html(plan_readings_formatted, "horner-classic-formatted", date_range)


if __name__ == "__main__":
    main()
