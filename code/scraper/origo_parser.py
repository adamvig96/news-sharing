def parse_soup(soup):

    try:
        title = soup.find("h1").get_text().strip()
    except AttributeError:
        title = ""

    try:
        author = soup.find(attrs={"class": "article-author"}).get_text().strip()
    except AttributeError:
        author = ""

    try:
        tags = soup.find(attrs={"id": "article-tags"}).get_text().strip()
    except AttributeError:
        tags = ""

    try:
        text = (
            soup.find(attrs={"id": "article-text"})
            .get_text()
            .replace("\n", " ")
            .replace("\xa0-", "")
            .strip()
        )
    except:
        text = ""

    try:
        urllist = str(
            [
                item.get("href")
                for item in soup.find(attrs={"id": "article-text"}).find_all("a")
                if item != None
            ]
        )

    except:
        urllist = ""

    return {
        "title": title,
        "author": author,
        "tags": tags,
        "text": text,
        "urllist": urllist,
    }
