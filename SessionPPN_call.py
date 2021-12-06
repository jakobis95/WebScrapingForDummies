
import requests
import json



def CPinfo(s):
    #Authentifizierungstoken wird aus json datei ausgelesen
    with open('token.txt', 'r') as jsonf:
        data = json.load(jsonf)
        print('Bearer ' + data['access_token'])


    url ='https://api.chargepoint-management.com/chargepoint/chargepoints/list?page=0&size=12&sort=masterData.chargePointName,asc&masterData.chargingFacilities.powerType=DC&status=INACTIVE'
    #Nachgebauter Header für Serveranfrage
    headers = {
        'authority' : 'api.chargepoint-management.com',
        'accept' : "application/json, text/plain, */*",
        'accept-encoding' : 'gzip, deflate, br',
        'accept-language' : 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'Origin' : 'https://www.chargepoint-management.com',
        'Referer':'https://www.chargepoint-management.com/',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Authorization' : "Baerer " + data['access_token']
        #'authorization' : 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJZbXROZ2d3OEh6R0lPa1o4Q2J5em5FVmZUWlAtYkIzckdXZ0FNYVpzVVA0In0.eyJleHAiOjE2Mzg1NTE5NzIsImlhdCI6MTYzODU1MTM3MiwiYXV0aF90aW1lIjoxNjM4NTQwOTc5LCJqdGkiOiJiNzU2MTFhMi00MGM1LTRiMTUtOGYxMS0yMmNhYWEyN2I4YjkiLCJpc3MiOiJodHRwczovL2xvZ2luLmNoYXJnZXBvaW50LW1hbmFnZW1lbnQuY29tL2F1dGgvcmVhbG1zL1BBRyIsImF1ZCI6WyJicm9rZXIiLCJhY2NvdW50Il0sInN1YiI6IjEyY2E3NDdiLTIzN2QtNDMzYy1hZmNjLTk3NTdmZmU5NmQxNCIsInR5cCI6IkJlYXJlciIsImF6cCI6ImNwb2MtZnJvbnRlbmQiLCJub25jZSI6ImQ5MDM2YTliLTczYzMtNDA0Ni04ZjhlLWIzNGFkNGMzOWNkOSIsInNlc3Npb25fc3RhdGUiOiJjNWVlN2JkZC03ZDM5LTQ2N2MtOGRhMy0yYjQzMzI3MTNjNDgiLCJhY3IiOiIwIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIlBfVklFV19DSEFSR0VQT0lOVF9NQVNURVJfREFUQSIsIkNQTyIsIlBfUkVTRVRfQ0hBUkdFUEFSS19FTEVNRU5UIiwiUF9WSUVXX0NPTkZJR1VSQVRJT05fT0ZfQ0hBUkdFUE9JTlQiLCJQX1ZJRVdfQ0hBUkdFUE9JTlRfVEVDSE5JQ0FMX1NFVFRJTkdTIiwiUF9WSUVXX0NIQVJHRV9UUkFOU0FDVElPTl9NT0RFU19JTlRFUk5BTCIsIlBfVklFV19IUENfRVJST1JfQ09ERSIsIlBfUkVTVEFSVF9DSEFSR0VQQVJLX0VMRU1FTlQiLCJQX0NIQU5HRV9DSEFSR0VfVFJBTlNBQ1RJT05fTU9ERVNfSFVCSkVDVCIsIlBfVklFV19UUkFOU0FDVElPTiIsIlBfVklFV19BQ0NPVU5UX0RBVEEiLCJQX1VQREFURV9GSVJNV0FSRSIsIlBfT05CT0FSRF9JTklUSUFMX0NQTyIsIm9mZmxpbmVfYWNjZXNzIiwiUF9DSEFOR0VfQ09ORklHVVJBVElPTl9PRl9DSEFSR0VQT0lOVCIsIlBfQ0hBTkdFX0NIQVJHRV9UUkFOU0FDVElPTl9NT0RFU19JTlRFUk5BTCIsIlBfVklFV19IUENfTUVBU1VSRU1FTlRTIiwiUF9WSUVXX0NIQVJHRV9UUkFOU0FDVElPTl9NT0RFU19IVUJKRUNUIiwidW1hX2F1dGhvcml6YXRpb24iLCJQX1ZJRVdfQ0hBUkdFUE9JTlRTX09WRVJWSUVXIiwiUF9WSUVXX0hQQ19PVkVSVklFVyIsIlBfVklFV19DSEFSR0VQT0lOVF9ERVRBSUxTIiwiUF9WSUVXX1BQTl9MSU5LIiwiUF9FRElUX0hQQ19DT05GSUdVUkFUSU9OIiwiUF9WSUVXX0hQQ19DT05GSUdVUkFUSU9OIiwiUF9DSEFOR0VfQUNDT1VOVF9EQVRBIiwiUF9DSEFOR0VfQ0hBUkdFUE9JTlRfT1BFTklOR19IT1VSU19BTkRfQVZBSUxBQklMSVRZIiwiUF9WSUVXX0VDT05PTUlDQUxfTUFOQUdFTUVOVCIsIkNQT0NfRVhQRVJUIiwiUF9WSUVXX0RJQUdOT1NJU19EQVRBIiwiUF9FRElUX0VDT05PTUlDQUxfTUFOQUdFTUVOVCIsIlBfVklFV19GSVJNV0FSRSIsIlBfQ0hBTkdFX0NIQVJHRVBPSU5UX01BU1RFUl9EQVRBIiwiUF9MT0dJTiIsIlBfVklFV19IUENfSURFTlRJRklDQVRJT04iLCJQX1NUQVJUX01BTlVBTF9UUkFOU0FDVElPTiIsIlBfUkVTVEFSVF9DSEFSR0VQT0lOVCIsIlBfREVMRVRFX0hQQ19FUlJPUl9NRU1PUlkiXX0sInJlc291cmNlX2FjY2VzcyI6eyJicm9rZXIiOnsicm9sZXMiOlsicmVhZC10b2tlbiJdfSwiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQiLCJzeXN0ZW1BY2Nlc3MiOnRydWUsInByZWZlcnJlZF91c2VybmFtZSI6ImZvNGE1b3kiLCJjcG9faWRzIjpbMiw0LDUsNiw3LDgsOSwxMCwxMSwxMiwxMywxNCwxNSwxNiwxNywxOCwxOSwyMCwyMSwyMiwyMywyNCwyNSwyNiwyNywyOCwyOSwzMCwzMSwzMiwzMywzNCwzNSwzNiwzNywzOCwzOSw0MCw0MSw0Miw0Myw0NCw0NSw0Niw0Nyw0OCw0OSw1MCw1MSw1Miw1Myw1NCw1NSw1Niw1Nyw1OCw1OSw2MCw2MSw2Miw2NCw2NSw2Niw2Nyw2OSw3MCw3MSw3Miw3Myw3NCw3NSw3Niw3Nyw3OCw3OSw4MCw4MSw4Miw4Myw4NCw4NSw4Niw4Nyw4OCw4OSw5MCw5MSw5Miw5Myw5NCw5NSw5Niw5Nyw5OCw5OSwxMDAsMTAxLDEwMiwxMDMsMTA0LDEwNSwxMDYsMTA3LDEwOCwxMDksMTEwLDExMSwxMTIsMTEzLDExNCwxMTUsMTE2LDExNywxMTgsMTE5LDEyMCwxMjEsMTIyLDEyMywxMjQsMTI1LDEyNiwxMjcsMTI4LDEyOSwxMzAsMTMxLDEzMiwxMzMsMTM0LDEzNSwxMzYsMTM3LDEzOCwxMzksMTQwLDE0MSwxNDIsMTQzLDE0NCwxNDUsMTQ2LDE0NywxNDgsMTQ5LDE1MCwxNTEsMTUyLDE1MywxNTQsMTU1LDE1NiwxNTcsMTU4LDE1OSwxNjAsMTYxLDE2MiwxNjMsMTY0LDE2NSwxNjYsMTY3LDE2OCwxNjksMTcwLDE3MSwxNzIsMTczLDE3NCwxNzUsMTc2LDE3NywxNzgsMTc5LDE4MCwxODEsMTgyLDE4MywxODQsMTg1LDE4NiwxODcsMTg4LDE4OSwxOTAsMTkxLDE5MiwxOTMsMTk0LDE5NSwxOTYsMTk3LDE5OCwxOTksMjAwLDIwMSwyMDIsMjAzLDIwNCwyMDUsMjA2LDIwNywyMDgsMjA5LDIxMSwyMTIsMjEzLDIxNCwyMTUsMjE3LDIxOCwyMTksMjIwLDIyMSwyMjIsMjIzLDIyNCwyMjUsMjI2LDIyNywyMjgsMjI5LDIzMCwyMzEsMjMyLDIzMywyMzQsMjM1LDIzNiwyMzcsMjM4LDIzOSwyNDAsMjQxLDI0MiwyNDMsMjQ0LDI0NSwyNDYsMjQ3LDI0OCwyNDksMjUwLDI1MSwyNTIsMjUzLDI1NCwyNTUsMjU2LDI1NywyNTgsMjU5LDI2MCwyNjEsMjYyLDI2MywyNjQsMjY1LDI2NiwyNjcsMjY4LDI2OSwyNzAsMjcxLDI3MiwyNzMsMjc0LDI3NSwyNzYsMjc3LDI3OCwyNzksMjgwLDI4MSwyODIsMjgzLDI4NCwyODUsMjg2LDI4NywyODgsMjg5LDI5MCwyOTEsMjkyLDI5MywyOTQsMjk1LDI5NiwyOTcsMjk4LDI5OSwzMDEsMzAyLDMwMywzMDQsMzA1LDMwNiwzMDcsMzA4LDMwOSwzMTAsMzExLDMxMiwzMTMsMzE0LDMxNSwzMTYsMzE3LDMxOCwzMTksMzIwLDMyMSwzMjIsMzIzLDMyNCwzMjUsMzI2LDMyNywzMjgsMzI5LDMzMCwzMzEsMzMyLDMzMywzMzQsMzM1LDMzNiwzMzcsMzM4LDMzOSwzNDAsMzQxLDM0MiwzNDMsMzQ0LDM0NSwzNDYsMzQ3LDM0OCwzNDksMzUwLDM1MSwzNTIsMzUzLDM1NCwzNTUsMzU2LDM1NywzNTgsMzU5LDM2MCwzNjEsMzYyLDM2MywzNjQsMzY1LDM2NiwzNjcsMzY4LDM2OSwzNzAsMzcxLDM3MywzNzQsMzc1LDM3NiwzNzgsMzc5LDM4MCwzODEsMzgyLDM4MywzODQsMzg1LDM4NiwzODcsMzg4LDM4OSwzOTAsMzkxLDM5MiwzOTMsMzk0LDM5NSwzOTYsMzk3LDM5OCwzOTksNDAwLDQwMSw0MDIsNDAzLDQwNCw0MDUsNDA2LDQwNyw0MDgsNDA5LDQxMCw0MTEsNDEyLDQxMyw0MTQsNDE1XSwibG9jYWxlIjoiZW4tVVMiLCJ1c2VySWQiOiIxMmNhNzQ3Yi0yMzdkLTQzM2MtYWZjYy05NzU3ZmZlOTZkMTQiLCJlbWFpbCI6ImZvNGE1b3kifQ.YRB7jSGkac66PCtX8fVHBqOWIvUhTprc_sPT3_PV8lmvGf8Pwvjf_qS_Wm1pI34s3FsAs0o84pXazJx3P2UC8VIpBlQh2J-P7GNLbXjZ0tAkoFY462qur3FWucoIZ-TcwL_xDD9KXyrlWOHQzDOzgRmWbITDctWYFygZCBhyvxu42sad_chOfXpFsnovi5rG11-kpk69lPmEYB6HjLX-UnXO4lkxjlsHfhwx5ksTia32-p4hGgaRwccwUKKHxSOtVfZkTACfXdEJ7kXNXDW7MfZ28ecTJzQSRxLyTQK0u3UgB7Atnw4jTdUd079ZTc6cff6kBMiH5rp9DJGVh5pgTw'
        }


    p = s.get(url, headers=headers, verify=False )
    print(p)
    with open('Info.txt', 'w') as f:
        f.write(p.text)

def refreshT(s): # Hier wird der Token refreshed
    #die verwendete Json datei wird aus dem Browser kopiert
    with open('token.txt', 'r') as jsonf:
        data = json.load(jsonf)
        print(data['refresh_token'])


    url = 'https://login.chargepoint-management.com/auth/realms/PAG/protocol/openid-connect/token'
    headers = {
        'authority' : 'api.chargepoint-management.com',
        'accept' : '*/*',
        'accept-encoding' : 'gzip, deflate, br',
        'accept-language' : 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'Origin' : 'https://www.chargepoint-management.com',
        'Referer':'https://www.chargepoint-management.com/',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        #'Cookie': 'AUTH_SESSION_ID=c5ee7bdd-7d39-467c-8da3-2b4332713c48.e3b7f9c6-acc3-4abe-7b3a-4903; AUTH_SESSION_ID_LEGACY=c5ee7bdd-7d39-467c-8da3-2b4332713c48.e3b7f9c6-acc3-4abe-7b3a-4903; KEYCLOAK_SESSION=PAG/12ca747b-237d-433c-afcc-9757ffe96d14/c5ee7bdd-7d39-467c-8da3-2b4332713c48; KEYCLOAK_SESSION_LEGACY=PAG/12ca747b-237d-433c-afcc-9757ffe96d14/c5ee7bdd-7d39-467c-8da3-2b4332713c48; KEYCLOAK_IDENTITY=eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJiODJmYzRkZC1iOGI5LTQyODQtYjZlNy0wMTg3NTRlYWFiMzAifQ.eyJleHAiOjE2Mzg1Nzk2MTAsImlhdCI6MTYzODU0MzYxMCwianRpIjoiMDdhMWQ4MDItZjRkYS00MDFlLWE5NWQtZGQ0NTYxMjg5ZmNlIiwiaXNzIjoiaHR0cHM6Ly9sb2dpbi5jaGFyZ2Vwb2ludC1tYW5hZ2VtZW50LmNvbS9hdXRoL3JlYWxtcy9QQUciLCJzdWIiOiIxMmNhNzQ3Yi0yMzdkLTQzM2MtYWZjYy05NzU3ZmZlOTZkMTQiLCJ0eXAiOiJTZXJpYWxpemVkLUlEIiwic2Vzc2lvbl9zdGF0ZSI6ImM1ZWU3YmRkLTdkMzktNDY3Yy04ZGEzLTJiNDMzMjcxM2M0OCIsInN0YXRlX2NoZWNrZXIiOiJqQmtNc0JRNFVMTFNiVnAwYzFTNVJocFVKbDNKZEpRcncwXzhPUEIxQVdVIn0.aXXwy4ZRfTTHXDcPKF3zLPM1J3ryYwzZkwhLWHqKltA; KEYCLOAK_IDENTITY_LEGACY=eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJiODJmYzRkZC1iOGI5LTQyODQtYjZlNy0wMTg3NTRlYWFiMzAifQ.eyJleHAiOjE2Mzg1Nzk2MTAsImlhdCI6MTYzODU0MzYxMCwianRpIjoiMDdhMWQ4MDItZjRkYS00MDFlLWE5NWQtZGQ0NTYxMjg5ZmNlIiwiaXNzIjoiaHR0cHM6Ly9sb2dpbi5jaGFyZ2Vwb2ludC1tYW5hZ2VtZW50LmNvbS9hdXRoL3JlYWxtcy9QQUciLCJzdWIiOiIxMmNhNzQ3Yi0yMzdkLTQzM2MtYWZjYy05NzU3ZmZlOTZkMTQiLCJ0eXAiOiJTZXJpYWxpemVkLUlEIiwic2Vzc2lvbl9zdGF0ZSI6ImM1ZWU3YmRkLTdkMzktNDY3Yy04ZGEzLTJiNDMzMjcxM2M0OCIsInN0YXRlX2NoZWNrZXIiOiJqQmtNc0JRNFVMTFNiVnAwYzFTNVJocFVKbDNKZEpRcncwXzhPUEIxQVdVIn0.aXXwy4ZRfTTHXDcPKF3zLPM1J3ryYwzZkwhLWHqKltA'
        }
    payload ={
        'grant_type':'refresh_token',
        'refresh_token' : data["refresh_token"],
        'client_id' : 'cpoc-frontend'
        }


    p = s.post(url, headers=headers, verify=False, data = payload )
    print(p)
    with open('token.txt', 'w') as f:
        f.write(p.text)

if __name__ == '__main__':
    #Session wird erstellt für konsistentes Cookie handling
    s = requests.Session()
    refreshT(s)
    CPinfo(s)

    with open('token.txt') as jsonf:
        token1 = json.load(jsonf)
        print(token1)
    print("ende")