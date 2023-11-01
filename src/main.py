import requests  # 「pip install requests」などが必要

if __name__ == '__main__':

    print("Run WebDriver")

    url = 'http://localhost:9515/session'
    res = requests.post(
        url,
        headers={'Content-Type': 'application/json'},
        data='{"capabilities":{}}'
    ).json()

    sessionId = res.get("value").get("sessionId")

    requests.delete(
        url + '/' + sessionId,
        headers={'Content-Type': 'application/json'},
    )
