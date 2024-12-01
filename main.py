import requests
import webbrowser
import urllib.parse


class WikipediaAPI:
    """
    Класс для взаимодействия с API Википедии.
    """

    BASE_URL = "https://ru.wikipedia.org/w/api.php"

    def search(self, query):
        """
        Выполняет поиск по запросу в Википедии.

        :param query: Строка, содержащая поисковый запрос.
        :return: JSON-ответ от API Википедии.
        """
        params = {
            "action": "query",
            "list": "search",
            "format": "json",
            "srsearch": query
        }
        response = requests.get(self.BASE_URL, params=params)
        return response.json()


class SearchResultParser:
    """
    Класс для парсинга результатов поиска из API Википедии.
    """

    @staticmethod
    def parse(data):
        """
        Извлекает результаты поиска из JSON-ответа.

        :param data: JSON-ответ от API Википедии.
        :return: Список статей, найденных по запросу.
        """
        if 'query' in data and 'search' in data['query']:
            return data['query']['search']
        return []


class ArticleOpener:
    """
    Класс для открытия статей Википедии в веб-браузере.
    """

    @staticmethod
    def open(page_id):
        """
        Открывает статью Википедии по указанному идентификатору страницы.

        :param page_id: Идентификатор страницы статьи в Википедии.
        """
        url = f"https://ru.wikipedia.org/w/index.php?curid={page_id}"
        webbrowser.open(url)


class WikipediaSearcher:
    """
    Класс для поиска статей в Википедии и открытия статьи.
    """

    def init(self, api, parser, opener):
        """
        Инициализирует экземпляр класса WikipediaSearcher.

        :param api: Экземпляр класса WikipediaAPI для выполнения запросов к API.
        :param parser: Экземпляр класса SearchResultParser для парсинга результатов.
        :param opener: Экземпляр класса ArticleOpener для открытия статей.
        """
        self.api = api
        self.parser = parser
        self.opener = opener

    def search_and_open_first_article(self):
        """
        Выполняет поиск по запросу и открывает статью.
        """
        query = input("Введите поисковый запрос: ")
        search_results = self.api.search(query)
        results = self.parser.parse(search_results)

        if results:
            first_article_id = results[0]['pageid']
            print(f"Открытие статьи: {results[0]['title']}")
            self.opener.open(first_article_id)
        else:
            print("Нет результатов по запросу")


def main():
    api = WikipediaAPI()
    parser = SearchResultParser()
    opener = ArticleOpener()

    searcher = WikipediaSearcher(api, parser, opener)

    searcher.search_and_open_first_article()


if __name__ == "__main__":
    main()
