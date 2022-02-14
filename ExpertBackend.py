import requests
def request(s):
    url = 'https://test.bematix.com/rest/chargePark'
    headers = {
        'authority': 'api.chargepoint-management.com',
        'accept': '*/*',
        'path' : '/rest/chargePark',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type' : 'application/json; charset=UTF-8',
        'Origin': 'https://test.bematix.com',
        'Referer': 'https://test.bematix.com',
        'x-requested-with': 'XMLHttpRequest',
        'cookie' : '.AspNetCore.HpcBackendServer=CfDJ8P5q6z_OkZZLg6iNecBDIp6QXAg1fQ1n-Qeju43XyDSXnmroZZtrBgpHPDJG0AwEskJ-7jCgcYPweFdfdplGsUE670b0kIupsEKz8k42Ws8lbN0IMefCkHFvAV4RpxHfofTvlBwKu_QSA2HzPFi1IufOPR16jTVP9B08cMRgZ-qLBFfjQiisuiCRpAJuDCg5d85YZkToAYXUKst2gstruPQoGKAyGjTbdYcxX_L-aVw174XxgA9g1pLI1TVlWZqyS2cng7DcODWA89Sl8qCZ6dvzlP6PQQJJu4z7_9i8sqexhPEFIpkLg5SmXYVIuQzgS1KI-HN0PrloHtTovDEz6iKE2-vQL1ZY4utLXo6wB3Ik7kgb3LfZV8wUIaQnXkFaE-o6pMfU019xuCYupP_6MmNkJ-RsoUlziIJyNkOqyLetCuEUo0YwVTbZM2vPYa6trfNQYr7xkbjVsgku6t1lmEDqJWrNJYPh91pXQ_QIu9GZon1Dw_DCMJibD5meU4OVYf7oIjRAPO_OOFbuBkfpinLUmfctfXXEqxPvO5rUTVNnV7ra5VE6la9mUzCkKxFQ42ul-KqGOq-Ijc-SYb-WVxzsHzH1tEtBPEXZEvFdTMy2RWpa4lcvY3djAXUwDS1PNoi7ttSDySfiGI924emQt6x26IH_yjYlFvVMSAbC0Fz0cizEMYucWvRL6E7DbI29tpukdS1ik7Z1y-EKmkIkjbrEpY_B2NWs_YAXL-G4eyKNOMZEMKTCLnm21_Iq3c2gHtjnpHVjUa5etPYwCOFSpn4yf6aenYSGX6QGnkqPYYn-sD-WWStfta71m4OpEA7D_oa3p4Dii1LW83Ih2TbJQJ5l7-erFTh1iPs3NUGeIp0OSBI23FLKjBqnwX7NrYPtHiAtjlNq5bh-ZmhlrnAOTlBd1FPYyJTinaVOaJASJ-w_JNrCKKpe_B3XefCMO58EQQZPiHQR__oKLp52FI3nXTn2Nl2Jje6Kf2vo4xdgY9acAItGxvwia54W2XSAxWR6xxrL3ts49rbkItAKI1GTGRJlw4N5No9gOVeIqKiHoOtC6izrT56mqKTn8EjcTRUgtmQHBD7byQQYjz6UNDJFKH8CxOa0PBikbkUKzWm4PAxrzzuhTYLmDru3gKvONT4h2USgD62k6wOi2zFFqZiQrL4',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        }
    payload = {"username": "SecDevelopment",
                "password": "CPC_IAmSuperAdmin#J1"
               }

    print(s.get(url, headers=headers).text)

def post_request(s):
    url = 'https://test.bematix.com/rest/send/DataTransfer/CONFIGURATIONS'
    headers = {
        'authority': 'test.bematix.com',
        'accept': '*/*',
        'scheme' : 'https',
        'path': '/rest/send/DataTransfer/CONFIGURATIONS',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json; charset=UTF-8',
        'Origin': 'https://test.bematix.com',
        'Referer': 'https://test.bematix.com',
        'x-requested-with': 'XMLHttpRequest',
        'cookie': '.AspNetCore.HpcBackendServer=CfDJ8P5q6z_OkZZLg6iNecBDIp6QXAg1fQ1n-Qeju43XyDSXnmroZZtrBgpHPDJG0AwEskJ-7jCgcYPweFdfdplGsUE670b0kIupsEKz8k42Ws8lbN0IMefCkHFvAV4RpxHfofTvlBwKu_QSA2HzPFi1IufOPR16jTVP9B08cMRgZ-qLBFfjQiisuiCRpAJuDCg5d85YZkToAYXUKst2gstruPQoGKAyGjTbdYcxX_L-aVw174XxgA9g1pLI1TVlWZqyS2cng7DcODWA89Sl8qCZ6dvzlP6PQQJJu4z7_9i8sqexhPEFIpkLg5SmXYVIuQzgS1KI-HN0PrloHtTovDEz6iKE2-vQL1ZY4utLXo6wB3Ik7kgb3LfZV8wUIaQnXkFaE-o6pMfU019xuCYupP_6MmNkJ-RsoUlziIJyNkOqyLetCuEUo0YwVTbZM2vPYa6trfNQYr7xkbjVsgku6t1lmEDqJWrNJYPh91pXQ_QIu9GZon1Dw_DCMJibD5meU4OVYf7oIjRAPO_OOFbuBkfpinLUmfctfXXEqxPvO5rUTVNnV7ra5VE6la9mUzCkKxFQ42ul-KqGOq-Ijc-SYb-WVxzsHzH1tEtBPEXZEvFdTMy2RWpa4lcvY3djAXUwDS1PNoi7ttSDySfiGI924emQt6x26IH_yjYlFvVMSAbC0Fz0cizEMYucWvRL6E7DbI29tpukdS1ik7Z1y-EKmkIkjbrEpY_B2NWs_YAXL-G4eyKNOMZEMKTCLnm21_Iq3c2gHtjnpHVjUa5etPYwCOFSpn4yf6aenYSGX6QGnkqPYYn-sD-WWStfta71m4OpEA7D_oa3p4Dii1LW83Ih2TbJQJ5l7-erFTh1iPs3NUGeIp0OSBI23FLKjBqnwX7NrYPtHiAtjlNq5bh-ZmhlrnAOTlBd1FPYyJTinaVOaJASJ-w_JNrCKKpe_B3XefCMO58EQQZPiHQR__oKLp52FI3nXTn2Nl2Jje6Kf2vo4xdgY9acAItGxvwia54W2XSAxWR6xxrL3ts49rbkItAKI1GTGRJlw4N5No9gOVeIqKiHoOtC6izrT56mqKTn8EjcTRUgtmQHBD7byQQYjz6UNDJFKH8CxOa0PBikbkUKzWm4PAxrzzuhTYLmDru3gKvONT4h2USgD62k6wOi2zFFqZiQrL4',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    payload = {"globalId": "0000000000000003010a",
               "data": {"key": "CP_DCMeter_Installed",
                        "value": "DCMeter not installed"},
               "vendorId": "",
               "messageId": "10"}

    print(s.post(url, headers=headers, data=payload).json())

if __name__ == '__main__':
    s = requests.session()
    post_request(s)