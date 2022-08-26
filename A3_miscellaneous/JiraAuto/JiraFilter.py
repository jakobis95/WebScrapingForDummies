# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json
url = "https://highway.porsche.com/jira/rest/auth/1/session"
#url = "https://jakobis95.atlassian.net/rest/api/3/search"

auth = HTTPBasicAuth("AJ2MSGR", "BrPFxvgYooXISA57fFAa70r3pipEnlNuB4WFQa")
#auth = HTTPBasicAuth("jakobis95@gmail.com", "D0vhqIK5DtgB8RS4xSfD33BC")

headers = {
   "Accept": "application/json"
}

query = {
   'jql': 'text ~ Fast'

}

response = requests.request(
   "GET",
   url,
   headers=headers,
   params=query,
   auth=auth
)
print(response.text)
print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))