import requests

url = "http://123.206.31.85:10003/"

querystring = {"op":"upload"}

payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"submit\"\r\n\r\nUpload!\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"image\"; filename=\"WX20190403-190512@2x.png\"\r\nContent-Type: image/png\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
headers = {
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'User-Agent': "",
    'Content-Type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache",
    'Postman-Token': "a403c3f8-16fa-4c1a-a25b-8fb340588ce5"
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

print(response.text)