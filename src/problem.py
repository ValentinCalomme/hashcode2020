from __future__ import annotations


class Problem:
    """Problem to solve"""

    def __init__(self, name: str, filename: Path):

        self.name = name
        self.filename = filename

        with open(self.filename, "r", encoding="utf-8") as file:

            self.raw = file.read()

        self.parse(self.raw)

    def get_row_data(self, row: str):
        return [int(value) for value in row.split(' ')]

    def parse(self, raw: str):
        """Parses the raw representation of the problem

        Parameters
        ----------
        raw : str
            text representation of the problem
        """

        rows = raw.split('\n')

        # Parse header
        header = self.get_row_data(rows[0])
        self.num_books      = header[0]  # B = Number of different books
        self.num_libraries  = header[1]  # L = Number of libraries
        self.num_days       = header[2]  # D =Number of days available
        self.book_scores = self.get_row_data(rows[1])  # Scores for each Book

        # Parse sections
        self.libraries = []
        for j in range(2, len(rows)-2, 2):
            if rows[j] == '':
                # For some reason the different data files are inconsistent and may contain 1 OR 2 empty lines at the end of the file (?)
                # Just skip empty lines..
                continue

            # Parse books in this library
            books_in_library = self.get_row_data(rows[j+1])  # List of book ids in this library
            books = [Book(book, self.book_scores[book]) for book in books_in_library]

            # Parse library info
            library_info = self.get_row_data(rows[j])   # Info about library
            Library_num_books = library_info[0]  # unused
            signup_process = library_info[1]
            books_per_day = library_info[2]
            library_id = int(j/2)

            self.libraries.append(Library(library_id, books, signup_process, books_per_day))


class Book:
    def __init__(self, book_id: int, book_score: int):

        self.book_id = book_id
        self.book_score = book_score

    def __hash__(self):

        return hash((self.book_id, self.book_score))


class Library:
    def __init__(
        self, library_id: int, books: List[Book], sign_up_time: int, books_per_day: int
    ):

        self.library_id = library_id
        self.books = sorted(books, key=lambda x: x.book_score, reverse=True)
        self.sign_up_time = sign_up_time
        self.books_per_day = books_per_day


class Time:
    def __init__(self, days: int):

        self.days = days
        self.current_day = 0
