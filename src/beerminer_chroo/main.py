import bs4
import requests
import re

from beer import Beer
from database import Database

# create database connection
database = Database("beers.db")
print(f"Database connection established to: {database}")

def construct_url(protocol, server, url) -> str:
    return protocol+"://"+server+url

def get_beer_list_atlas(protocol, server, url) -> list:
    print(f"Fetching beers from: {construct_url(protocol, server, url)}")

    response = requests.get(construct_url(protocol, server, url))
    response.encoding = response.apparent_encoding
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    all_rows = soup.find_all('tr')
    progress = 0
    complete = len(all_rows)

    for beer in all_rows:
        # show progress
        print(f"Progress: {'█'*(progress//(complete // 10))}{' '*(10-progress//(complete // 10))} {progress}/{complete}", end="\r")
        progress += 1

        beer_name_tag = beer.find('a', class_='beername hinted')
        if not beer_name_tag:
            continue

        beer_name = beer_name_tag.text.strip()
        beer_url = construct_url(protocol, server, beer_name_tag['href'])
        beer_style = beer.find_all('td')[-1].text.strip()
        beer_rating = beer.find_all('span', class_='invisible')[-1].text.strip() + "/10"

        # follow to the detail page to get more information
        response = requests.get(beer_url)
        response.encoding = response.apparent_encoding
        beer_soup = bs4.BeautifulSoup(response.text, 'html.parser')

        # get beer percentage
        try:
            beer_abv = re.search(r'\d+\.\d+\s?%',beer_soup.find_all('tr')[4].text.strip()).group().replace('%', '')
        except AttributeError:
            beer_abv = "N/A"

        # get beer epm
        try:
            beer_epm = re.search(r'\d+\.\d+\s?°',beer_soup.find_all('tr')[6].text.strip()).group().replace('°', '')
        except AttributeError:
            beer_epm = "N/A"

        # get beer brewery
        try:
            beer_brewery = beer_soup.find('span', {"id": "brewery_name_result"}).find('a').text.strip()
        except AttributeError:
            beer_brewery = "N/A"

        # get beer location
        try:
            beer_location = beer_soup.find('span', {"id": "brewery_name_result"}).text.replace(beer_brewery, "")[1::].strip()
        except AttributeError:
            beer_location = "N/A"

        # get beer description
        try:
            beer_description = beer_soup.find('i').text.strip()
        except AttributeError:
            beer_description = "N/A"

        beer = Beer(beer_name)
        beer.set('style', beer_style)
        beer.set('abv', beer_abv)
        beer.set('epm', beer_epm)
        beer.set('brewery', beer_brewery)
        beer.set('location', beer_location)
        beer.set('description', beer_description)
        beer.set('url', beer_url)
        beer.set('image_url', None)
        beer.set('rating', beer_rating)

        # insert into database
        db_beer = database.find_fuzzy(beer)

        if not db_beer:
            # print(f"Inserting beer: {beer.name}")
            database.insert(beer)
        else:
            # print(f"Beer already exists: {beer.name}")
            db_beer = db_beer[0]
            db_beer_id = db_beer[0]

            update_object = Beer(db_beer[1])
            if db_beer[2] == "N/A" or db_beer[2] == None:
                update_object.set('style', beer_style)
            else:
                update_object.set('style', db_beer[2])

            if db_beer[3] == "N/A" or db_beer[3] == None:
                update_object.set('abv', beer_abv)
            else:
                update_object.set('abv', db_beer[3])

            if db_beer[4] == "N/A" or db_beer[4] == None:
                update_object.set('epm', beer_epm)
            else:
                update_object.set('epm', db_beer[4])

            if db_beer[6] == "N/A" or db_beer[6] == None:
                update_object.set('brewery', beer_brewery)
            else:
                update_object.set('brewery', db_beer[6])

            if db_beer[7] == "N/A" or db_beer[7] == None:
                update_object.set('location', beer_location)
            else:
                update_object.set('location', db_beer[7])

            if db_beer[8] == "N/A" or db_beer[8] == None:  
                update_object.set('description', beer_description)
            else:
                update_object.set('description', db_beer[8])

            if db_beer[9] == "N/A" or db_beer[9] == None:
                update_object.set('url', beer_url)
            else:
                update_object.set('url', db_beer[9])

            if db_beer[10] == "N/A" or db_beer[10] == None:
                update_object.set('rating', beer_rating)
            else:
                update_object.set('rating', db_beer[10])

            database.update(db_beer_id, update_object)

    return database.fetch()

def get_beer_list_pivnici(protocol, server, url) -> list:
    print(f"Fetching beers from: {construct_url(protocol, server, url)}")

    resource = requests.get(construct_url(protocol, server, url))
    resource.encoding = resource.apparent_encoding
    soup = bs4.BeautifulSoup(resource.text, 'html.parser')

    # check if there is a pagination
    pagination = soup.find('div', class_='paging controls')
    actual_page = int(pagination.find('span', class_='actual').text)
    last_page = int(pagination.find_all('a')[-1].text)
    print(f"Website has: {last_page} pages")

    for page in range(actual_page, last_page+1):
        try:
            if page != 1:
                page_url = construct_url(protocol, server, url + f'strana-{page}/')
            else:
                page_url = construct_url(protocol, server, url)

            resource = requests.get(page_url)
            resource.encoding = resource.apparent_encoding
            soup = bs4.BeautifulSoup(resource.text, 'html.parser')

            all_rows = soup.find('div', class_='list')
            all_rows = all_rows.find_all('div', class_='item')

            progress = 0
            complete = len(all_rows)
            print(f'Fetching beers from page: {page} of {last_page}')

            for beer in all_rows:
                # show progress
                print(f"Progress: {'█'*(progress//(complete // 10))}{' '*(10-progress//(complete // 10))} {progress}/{complete}", end="\r")
                progress += 1

                # get beer name
                try:
                    beer_name = beer.find('span', class_='label').find('a').text.strip()
                except AttributeError:
                    continue

                # follow to the detail page to get more information
                beer_url = construct_url(protocol, server, beer.find('span', class_='label').find('a')['href'])
                response = requests.get(beer_url)
                response.encoding = response.apparent_encoding
                beer_soup = bs4.BeautifulSoup(response.text, 'html.parser')

                details = beer_soup.find('div', class_='itemDetails first')

                # get beer rating
                try:
                    beer_rating = details.find('div', class_='rating').find('span', class_="min").text.strip().replace(',', '.')
                except AttributeError:
                    beer_rating = "N/A"

                # get beer style
                try:
                    beer_style = details.find('span', string='Pivní styl:')           
                    beer_style = beer_style.parent.text
                    beer_style_start = beer_style.find(':')
                    beer_style = beer_style[beer_style_start+1::].strip()
                except AttributeError:
                    beer_style = "N/A"
                    
                # get abv
                try:
                    beer_abv = details.find('span', string='Obsah alkoholu:')
                    beer_abv = beer_abv.parent.text
                    beer_abv_start = beer_abv.find(':')
                    beer_abv = beer_abv[beer_abv_start+1::].strip().replace(',', '.')
                except AttributeError:
                    beer_abv = "N/A"

                # get epm
                try:
                    beer_epm = details.find('span', string='Stupňovitost:')
                    beer_epm = beer_epm.parent.text
                    beer_epm_start = beer_epm.find(':')
                    beer_epm = beer_epm[beer_epm_start+1::].strip().replace(',', '.')
                except AttributeError:
                    beer_epm = "N/A"

                # get brewery
                try:
                    beer_brewery = details.find('span', string='Pivovar:')
                    beer_brewery = beer_brewery.parent.text
                    beer_brewery_start = beer_brewery.find(':')
                    beer_brewery_end = beer_brewery.find('(')
                    beer_brewery_name = beer_brewery[beer_brewery_start+1:beer_brewery_end].strip()

                # get location
                    beer_location = beer_brewery[beer_brewery_end::].replace('(', "").replace(")", "").strip()
                except AttributeError:
                    beer_brewery_name = "N/A"
                    beer_location = "N/A"

                beer = Beer(beer_name)
                beer.set('style', beer_style)
                beer.set('abv', beer_abv)
                beer.set('epm', beer_epm)
                beer.set('brewery', beer_brewery_name)
                beer.set('location', beer_location)
                beer.set('description', 'N/A')
                beer.set('url', beer_url)
                beer.set('image_url', 'N/A')
                beer.set('rating', beer_rating)

                # insert into database
                db_beer = database.find_fuzzy(beer)

                if not db_beer:
                    database.insert(beer)
                else:
                    db_beer = db_beer[0]
                    db_beer_id = db_beer[0]

                    update_object = Beer(db_beer[1])
                    if db_beer[2] == "N/A" or db_beer[2] == None:
                        update_object.set('style', beer_style)
                    else:
                        update_object.set('style', db_beer[2])

                    if db_beer[3] == "N/A" or db_beer[3] == None:
                        update_object.set('abv', beer_abv)
                    else:
                        update_object.set('abv', db_beer[3])

                    if db_beer[4] == "N/A" or db_beer[4] == None:
                        update_object.set('epm', beer_epm)
                    else:
                        update_object.set('epm', db_beer[4])
                        
                    if db_beer[6] == "N/A" or db_beer[6] == None:
                        update_object.set('brewery', beer_brewery_name)
                    else:
                        update_object.set('brewery', db_beer[6])

                    if db_beer[7] == "N/A" or db_beer[7] == None:
                        update_object.set('location', beer_location)
                    else:
                        update_object.set('location', db_beer[7])

                    if db_beer[8] == "N/A" or db_beer[8] == None:  
                        update_object.set('description', 'N/A')
                    else:
                        update_object.set('description', db_beer[8])

                    if db_beer[9] == "N/A" or db_beer[9] == None:
                        update_object.set('url', beer_url)
                    else:
                        update_object.set('url', db_beer[9])

                    if db_beer[10] == "N/A" or db_beer[10] == None:
                        update_object.set('rating', beer_rating)
                    else:
                        update_object.set('rating', db_beer[10])

                    database.update(db_beer_id, update_object)

        except Exception as e:  
            print(e)
            raise
        
    return database.fetch()



if __name__ == "__main__":    
    get_beer_list_atlas("http","www.atlaspiv.cz/","?page=hodnoceni")
    get_beer_list_pivnici("https","www.pivnici.cz/","seznam/piva/dle-alkoholu/")

