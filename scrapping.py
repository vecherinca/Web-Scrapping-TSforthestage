import requests 
from bs4 import BeautifulSoup
import re
from csv import writer

def get_the_number_of_page(URL):
    """

    This function extracts the number of
    pages by every given arrondisment. As 
    the total number of pages is given to 
    us in "pagination__button pagination__page"
    section.

    As an argument it takes the URL. 

    """
    lst = []
    numbers = []
    page = requests.get(URL)
    html = page.content
    soup = BeautifulSoup(html, 'lxml')
    for div in soup.find_all('a', class_ = "pagination__button pagination__page"):
        lst.append(div)
    for elements in lst:
        numbers += re.findall(r'data-paginate-page-num="(\d+)"', str(elements))
    num = int(numbers[-1])
    return(num)

def get_the_index(arr):
    """
    In our database we need to define the identifiant de l’arrondissement.
    As it wasn't present in a section that I chosed, I decided to to do it manually,
    using the arrondisment data from the source code. It may be a bit naive as
    a method, but it works :)

    """
    if arr == '                    Paris 1er arrondissement                ':
        arr = 32682
    if arr == '                    Paris 2ème arrondissement                ':
        arr = 32683
    if arr == '                    Paris 3ème arrondissement                ':
        arr = 32684
    if arr == '                    Paris 4ème arrondissement                ':
        arr = 32685
    if arr == '                    Paris 5ème arrondissement                ':
        arr = 32686
    if arr == '                    Paris 6ème arrondissement                ':
        arr = 32687
    if arr == '                    Paris 7ème arrondissement                ':
        arr = 32688
    if arr == '                    Paris 8ème arrondissement                ':
        arr = 32689
    if arr == '                    Paris 9ème arrondissement                ':
        arr = 32690
    if arr == '                    Paris 10ème arrondissement                ':
        arr = 32691
    if arr == '                    Paris 11ème arrondissement                ':
        arr = 32692
    if arr == '                    Paris 12ème arrondissement                ':
        arr = 32693
    if arr == '                    Paris 13ème arrondissement                ':
        arr = 32694
    if arr == '                    Paris 14ème arrondissement                ':
        arr = 32695
    if arr == '                    Paris 15ème arrondissement                ':
        arr = 32696
    if arr == '                    Paris 16ème arrondissement                ':
        arr = 32697
    if arr == '                    Paris 17ème arrondissement                ':
        arr = 32698
    if arr == '                    Paris 18ème arrondissement                ':
        arr = 32699
    if arr == '                    Paris 19ème arrondissement                ':
        arr = 32700
    if arr == '                    Paris 20ème arrondissement                ':
        arr = 32701

    return(arr)

def get_the_area(area):
    """
    This function is extracting an area of apartament size using the regex.
    Note:sometimes there is no area. That is why it was decided to put 1. 
    """
    area_pattern = r'(\d+) m²'
    try:
        area_room = re.search(area_pattern, str(area)).group(1)
    except Exception as e:
        area_room = 'NaN'
    if area_room == 'NaN':
        area_room = 1
    return(area_room)

def get_the_roomcount(area):
   """
   This function is takes the area of a room. 
   If there is a Studio, the 1 set as room count. 
   Else we scrap the number using regex.
   Note: sometimes the room_count is not defined.
   """
   
   studiostr = "Studio"
   if studiostr in area:
       room_count = 1
       return(room_count)
   else:
       try:
           room_count_pattern = r'(\d+) pièce'
           room_count = re.search(room_count_pattern, str(area)).group(1)
       except Exception as e:
           room_count = 'NaN'
       if room_count == 'NaN':
           room_count = 1
       return(room_count)

        
def get_the_data(parsed_data):
    """
    The get_the_data() function operates with the arguments that
    is gonna be in a dataset.
    As in some cases the price is not defined, it was decided
    to use the the exception handling.
    Also, this nice function transforms the data to csv table.
    It was also decided to put price at 1 and then drop the columns with the
    price 1 from the db. However another aproach could be done: it is
    possible to calculate mean by every arrondissment and put it instead of
    the of the 1.
    """
    with open('data_Jan6.csv', "w", encoding = 'utf8', newline = '') as f:
        thewriter = writer(f)
        header = ['listing_id', 'place_id', 'price','area', 'room_count']
        thewriter.writerow(header)

        for list in parsed_data:
            try:
                price = list.find('div', class_ = "listing-price margin-bottom").text.replace(u' ', u'').replace(u'\n', u'').replace(u'\u202f', u' ').replace(u'\xa0', u' ').replace(u' €', u'')
            except Exception as e:
                price = 'NaN'
            if price!='NaN':
                price = price.replace(' ', '')
            else:
                price = 1
            price = int(price)
            listing_id = list.find('button', attrs = {'class': "btn-reset listing-actions__item"})['data-listing-id']
            area_ = list.find('div', class_ = "listing-characteristic margin-bottom").text.replace(u'\xa0', u' ').replace(u'\n', u'')
            arr = list.find('div', class_ = "text--muted text--small").text.replace(u'\xa0', u' ').replace(u'\n', u'')
            arr = get_the_index(arr)
            area = get_the_area(area_)
            room_count = get_the_roomcount(area_)
            table = [listing_id, arr, price, area, room_count]
            thewriter.writerow(table)
        

"""
what did I do first is I created a list
where I will collect all the data
from the first 'listing-item__content' section 
"""
lists = []
for i in range(32682,32702):#iteration by arrondissment 
    URL = f"https://www.meilleursagents.com/annonces/achat/search/?item_types=ITEM_TYPE.APARTMENT&place_ids={i}&page={1}"
    num_page = get_the_number_of_page(URL)
    for j in range(1, num_page+1): #iteration by page
        URL = f"https://www.meilleursagents.com/annonces/achat/search/?item_types=ITEM_TYPE.APARTMENT&place_ids={i}&page={j}"
        page = requests.get(URL)
        html = page.content
        soup = BeautifulSoup(html, "lxml")
        for div in soup.find_all('div', class_ = 'listing-item__content'):
            lists.append(div)

get_the_data(lists)