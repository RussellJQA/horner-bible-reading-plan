import csv
import datetime
from pathlib import Path


def create_playlists():
    """Creates .m3u playlists from the plan, for use with Talking Bible International's KJV CD audio files"""
    book_nums: dict[str, int] = {}
    with open("bible_book_info.csv", "r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for book_count, row in enumerate(reader, start=1):
            book_nums[row["book"]] = book_count

    with open("horner_classic-20230101-20231231.csv", "r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        Path("m3us").mkdir(exist_ok=True)
        for row in reader:
            date = datetime.date(int(row["Date"][:4]), int(row["Date"][5:7]), int(row["Date"][8:10]))
            # Example m3u_filenames: "20230101-LD.m3u", "20230102-mon.m3u"
            m3u_filename = Path("m3us") / f"{date.strftime('%Y%m%d-%a').lower().replace('sun', 'LD')}.m3u"
            with open(m3u_filename, "w", encoding="utf-8") as m3u_file:
                m3u_file.write("#EXTM3U\n")
                m3u_file.write(f"#PLAYLIST:{date.strftime('%A, %d %B %Y').replace(' 0', ' ')}\n")
                m3u_file.write("#EXTALB: KJV Bible\n")
                m3u_file.write("#EXTART: Talking Bibles International\n")
                m3u_file.write("EXTGENRE:Speech\n")
                for grouping, reading in row.items():
                    if grouping != "Date":
                        book_len = len("Song of Songs") if reading[:13] == "Song of Songs" else reading.find(" ", 2)
                        book: str = reading[:book_len]
                        testament: str = "ot" if book_nums[book] < 40 else "nt"
                        book_num: str = str(book_nums[book] if testament == "ot" else book_nums[book] - 39).zfill(2)
                        chapter: str = reading[book_len + 1 :]
                        m3u_file.write(f"#EXTINF:0,{book} {chapter}\n")
                        book_for_filename = book.replace("Song of Songs", "songofsolomon").replace(" ", "-").lower()
                        mp3_filepath = Path(f"{testament}") / f"{book_num}_{book_for_filename}"
                        chapter_for_filename = chapter.zfill(3 if testament == "ot" else 2)
                        mp3_filename = mp3_filepath / f"{book_num}_{book_for_filename}_{chapter_for_filename}.mp3"
                        m3u_file.write(f"{mp3_filename}\n")


def main():
    create_playlists()


if __name__ == "__main__":
    main()
