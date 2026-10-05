import httpx

def get_post():
    url = "https://jsonplaceholder.typicode.com/posts/1"
    resp = httpx.get(url)
    print("状态码:", resp.status_code)
    print("返回内容:", resp.json())

get_post()
