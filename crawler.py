from bs4 import BeautifulSoup
import requests
import json

news_url = 'https://www.qdnd.vn/quoc-phong-an-ninh'

def crawler():
    base_url = "https://www.qdnd.vn/quoc-phong-an-ninh"

    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Kiểm tra mã trạng thái HTTP
    except requests.exceptions.RequestException as e:
        print(f"Lỗi: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    urls = [a['href'] for a in soup.select("article a") if 'href' in a.attrs]

    return urls

def get_content(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.select_one("h1.post-title").get_text(strip=True) if soup.select_one("h1.post-title") else "No Title Found"

    avatar = soup.select_one("img.imgtelerik")["src"] if soup.select_one("img.imgtelerik") else "No Avatar Found"

    summary = soup.select_one("p.logo-online").get_text(strip=True) if soup.select_one("p.logo-online") else "No Summary Found"

    article_body = soup.select_one('div[itemprop="articleBody"]')
    if article_body:
        for tag in article_body.find_all(True):
            if "class" in tag.attrs:
                del tag.attrs["class"]
            if "style" in tag.attrs:
                del tag.attrs["style"]

        # Lấy HTML đã được làm sạch
        article_body_clean_html = article_body
        
    else:
        print("No Article Body Found")

    return {
        "title": title,
        "img": avatar,
        "summary": summary,
        "original_url": url,
        "article_text": str(article_body_clean_html)
    }

if __name__ == "__main__":
    urls = crawler()
    data = []
    for url in urls:
        data.append(get_content(url))
    
    file_path = "articles.json"

    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)