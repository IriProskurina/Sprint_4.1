from main import BooksCollector
import pytest


# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        collector.add_new_book("Гордость и предубеждение и зомби")
        collector.add_new_book("Что делать, если ваш кот хочет вас убить")

        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
        assert len(collector.get_books_rating()) == 2


class TestBooksCollectorNew:
    @pytest.fixture
    def collector(self):
        return BooksCollector()

    @pytest.mark.parametrize(
        "book_name, expected",
        [("Война миров", True), ("Сияние", True), ("", False), ("A" * 41, False)],
    )
    def test_add_new_book(self, collector, book_name, expected):
        collector.add_new_book(book_name)
        assert (book_name in collector.get_books_genre()) == expected

    @pytest.mark.parametrize(
        "book_name, genre, expected_genre",
        [
            ("Война миров", "Фантастика", "Фантастика"),
            ("Сияние", "Ужасы", "Ужасы"),
            ("Война миров", "Неизвестный жанр", ""),
            ("Такой книги нет", "Фантастика", None),
        ],
    )
    def test_set_book_genre(self, collector, book_name, genre, expected_genre):
        collector.add_new_book("Война миров")
        collector.add_new_book("Сияние")
        collector.set_book_genre(book_name, genre)
        assert collector.get_book_genre(book_name) == expected_genre

    @pytest.mark.parametrize(
        "book_name, genre, expected",
        [
            ("Война миров", "Фантастика", "Фантастика"),
            ("Сияние", "Ужасы", "Ужасы"),
            ("Такой книги нет", None, None),
        ],
    )
    def test_get_book_genre(self, collector, book_name, genre, expected):
        if book_name != "Такой книги нет":
            collector.add_new_book(book_name)
            collector.set_book_genre(book_name, genre)
        result = collector.get_book_genre(book_name)
        assert result == expected

    @pytest.mark.parametrize(
        "books, genre, expected",
        [
            ([("Война миров", "Фантастика"), ("Сияние", "Ужасы")], "Фантастика", ["Война миров"]),
            ([("Война миров", "Фантастика"), ("Сияние", "Ужасы")], "Ужасы", ["Сияние"]),
            ([("Война миров", "Фантастика"), ("Сияние", "Ужасы")], "Детективы", []),
        ],
    )
    def test_get_books_with_specific_genre(self, collector, books, genre, expected):
        for book_name, book_genre in books:
            collector.add_new_book(book_name)
            collector.set_book_genre(book_name, book_genre)
        result = collector.get_books_with_specific_genre(genre)
        assert result == expected

    @pytest.mark.parametrize(
        "books, expected",
        [
            ([("Война миров", "Фантастика"), ("Сияние", "Ужасы")], ["Война миров"]),
            ([("Война миров", "Фантастика"), ("Шерлок Холмс", "Детективы")], ["Война миров"]),
            ([("Русалочка", "Мультфильмы"), ("Вокруг света за 80 дней", "Комедии")], ["Русалочка", "Вокруг света за 80 дней"]),
        ],
    )
    def test_get_books_for_children(self, collector, books, expected):
        for book_name, book_genre in books:
            collector.add_new_book(book_name)
            collector.set_book_genre(book_name, book_genre)
        result = collector.get_books_for_children()
        assert result == expected

    @pytest.mark.parametrize(
        "book_name, expected",
        [
            ("Война миров", True),
            ("Сияние", True),
            ("Такой книги нет", False),
        ],
    )
    def test_add_book_in_favorites(self, collector, book_name, expected):
        if book_name != "Такой книги нет":
            collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        result = book_name in collector.get_list_of_favorites_books()
        assert result == expected

    @pytest.mark.parametrize(
        "initial_favorites, book_to_remove, expected",
        [
            (["Война миров", "Сияние"], "Война миров", ["Сияние"]),
            (["Война миров", "Сияние"], "Сияние", ["Война миров"]),
            (["Война миров", "Сияние"], "Такой книги нет", ["Война миров", "Сияние"]),
        ],
    )
    def test_delete_book_from_favorites(
        self, collector, initial_favorites, book_to_remove, expected
    ):
        for book in initial_favorites:
            collector.add_new_book(book)
            collector.add_book_in_favorites(book)
        collector.delete_book_from_favorites(book_to_remove)
        result = collector.get_list_of_favorites_books()
        assert result == expected

    @pytest.mark.parametrize(
        "books, favorites, expected",
        [
            ([("Война миров", "Фантастика"), ("Сияние", "Ужасы")], ["Война миров"], ["Война миров"]),
            ([("Война миров", "Фантастика"), ("Сияние", "Ужасы")], ["Война миров", "Сияние"], ["Война миров", "Сияние"]),
            ([("Война миров", "Фантастика")], [], []),
        ],
    )
    def test_get_list_of_favorites_books(self, collector, books, favorites, expected):
        for book_name, genre in books:
            collector.add_new_book(book_name)
            collector.set_book_genre(book_name, genre)
        for favorite in favorites:
            collector.add_book_in_favorites(favorite)
        result = collector.get_list_of_favorites_books()
        assert result == expected

    @pytest.mark.parametrize(
        "books, expected",
        [
            (
                [("Война миров", "Фантастика"), ("Сияние", "Ужасы")],
                {"Война миров": "Фантастика", "Сияние": "Ужасы"},
            ),
            ([("Шерлок Холмс", "Детективы")], {"Шерлок Холмс": "Детективы"}),
            ([], {}),
        ],
    )
    def test_get_books_genre(self, collector, books, expected):
        for book_name, genre in books:
            collector.add_new_book(book_name)
            collector.set_book_genre(book_name, genre)
        result = collector.get_books_genre()
        assert result == expected

    @pytest.mark.parametrize(
        "book_name, genre, expected",
        [
            ("Война миров", "Фантастика", True),
            ("Сияние", "Ужасы", True),
            ("Такой книги нет", "Фантастика", False),
        ],
    )
    def test_add_and_get_favorites(self, collector, book_name, genre, expected):
        if book_name != "Такой книги нет":
            collector.add_new_book(book_name)
            collector.set_book_genre(book_name, genre)
            collector.add_book_in_favorites(book_name)
        result = book_name in collector.get_list_of_favorites_books()
        assert result == expected
