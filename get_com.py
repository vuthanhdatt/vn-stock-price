import requests
from bs4 import BeautifulSoup


def get_all_com_token(cookies, headers):
    '''
    Get token session to make request to api
    '''
    sess = requests.Session()
    url = 'https://finance.vietstock.vn/doanh-nghiep-a-z?page=1'
    r= sess.get(url,headers=headers, cookies=cookies)
    soup = BeautifulSoup(r.content, 'html5lib')
    token = soup.findAll('input', attrs={'name':'__RequestVerificationToken'})[0]['value']
    return token

def make_all_com_form(exchange,token, page):
    '''
    Make form to call to api
    '''
    catID = {'all': '0' ,'hose':'1','hnx':'2','upcom':'5'}
 
    f = {'catID': catID[exchange],
    'industryID': '0',
    'page':str(page),
    'pageSize': '50',
    'code':'',
    'businessTypeID':'0',
    'orderBy': 'Code',
    'orderDir': 'ASC',
    '__RequestVerificationToken':token}
    return f

def get_all_com(exchange, cookies, headers):
    '''
    Return all companies on choosen exchange.

    
    '''
    url = 'https://finance.vietstock.vn/data/corporateaz'
    token = get_all_com_token(cookies,headers)
    page = 1
    result = []
    while True:
        f = make_all_com_form(exchange, token, page)
        r = requests.post(url, headers=headers,cookies=cookies,data=f)
        if len(r.json()) != 0:
            for com in r.json():
                result.append(com['Code'])
            page +=1
        else:
            break
    return result
if __name__ == '__main__':
    # print(len(get_all_com('hose',cookie,header)))
    pass

    

