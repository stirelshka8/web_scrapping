import bs4
import requests
from fake_headers import Headers


def startup_programm():
    keywords = ['дизайн', 'фото', 'web', 'python', 'Блог']
    host = 'https://habr.com/ru/all'
    header = Headers(browser='chrome', os='win', headers=True).generate()
    out_req = requests.get(host, headers=header)
    in_req = out_req.text

    parser_ = bs4.BeautifulSoup(in_req, features='html.parser')
    articles = parser_.findAll('article')

    match_dictionary = []

    for data_art in articles:
        hubs = data_art.findAll('a', {"class": "tm-article-snippet__hubs-item-link"})
        hubs = [hub.span.text.lower() for hub in hubs]

        match_ = False
        matching_ = [hub for hub in hubs for key in keywords if key in hub]

        # Проверяем есть ли совпадения по ключевым словам
        if len(matching_):
            match_ = True

        if match_:
            title = data_art.find("a", {"class": "tm-article-snippet__title-link"})
            date = data_art.find("span", {"class": "tm-article-snippet__datetime-published"})
            match_dictionary.append({
                "title": title.span.text,
                "ref": host + title["href"],
                "datetime": date.time["datetime"],
                "matching": matching_
            })

    for sort_data in match_dictionary:
        print(f"'{sort_data['datetime']} - {sort_data['title']} - {sort_data['ref']}")


if __name__ == '__main__':
    startup_programm()
