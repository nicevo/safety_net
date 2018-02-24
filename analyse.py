import requests

text = "bla bla asshole ..."
r = requests.post("https://ca-image-analyzer.herokuapp.com/api/analyses",
                  json={"analysis": {"resource": text, "category": "text"}})
print(print(r.status_code, r.reason))
print(r.json()['results']['value']== 'Non-Adult')
