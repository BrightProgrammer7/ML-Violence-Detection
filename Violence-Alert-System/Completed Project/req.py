import requests

url = "http://127.0.0.1:8000/detect_violence"

payload = {}
files=[
  ('video',('D:\code\VD\Violence-Alert-System\Completed Project\V_19.mp4',open('D:\\code\\VD\\Violence-Alert-System\\Completed Project\\V_19.mp4','rb'),'application/octet-stream'))
]
headers = {}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)
