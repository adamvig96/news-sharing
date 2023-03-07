def parse_soup(self, soup):
    # Title
    try:
        title = soup.find(attrs={"itemprop": "headline"}).get_text().strip()
    except:
        title = ""
    # Text
    try:
        textlist = (
            [soup.find(attrs={"data-ce-measure-widget": "Cikk lead"})]
            + soup.find(attrs={"class": "o-post__body o-postCnt post-body"}).find_all(
                "p"
            )
            + soup.find(attrs={"class": "o-post__body o-postCnt post-body"}).find_all(
                "li"
            )
        )
        text = (
            " ".join([item.get_text().strip() for item in textlist if item != None])
            .replace("\xa0", "")
            .strip()
        )
    except:
        text = ""
    # Author
    try:
        author = soup.find(attrs={"class": "m-author__name"}).get_text()
    except:
        author = ""
    # tags
    try:
        taglist = soup.find_all(
            attrs={"class": "m-tag__links a-tag -articlePageMainTags swiper-slide"}
        )
        tags = str([item.get_text().strip().lower() for item in taglist])
    except:
        tags = ""

    try:
        urllist = [
            item.find_all("a")
            for item in soup.find(
                attrs={"class": "o-post__body o-postCnt post-body"}
            ).find_all("p")
        ]
        urllist = str([x.get("href") for l in urllist for x in l])

    except:
        urllist = ""

    return {
        "title": title,
        "author": author,
        "tags": tags,
        "text": text,
        "urllist": urllist,
    }
