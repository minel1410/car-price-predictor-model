import requests
from collections import Counter
import csv

import csv
import requests

import requests
import csv

import csv
import requests

def fetch_article_and_write_to_file(loading_file, file_path, start_id, number_of_articles):
    base_url = "https://olx.ba/api/listings/"

    with open(loading_file, 'r', encoding='utf-8') as f:
        ids = [line.strip() for line in f.readlines()]

    start_index = ids.index(str(start_id))
    ids_to_process = ids[start_index:start_index + number_of_articles]

    with open(file_path, 'a+', newline='', encoding='utf-8') as csvfile:
        csvfile.seek(0)
        first_char = csvfile.read(1)
        if not first_char:
            writer = csv.writer(csvfile)
            header = ['Brand', 'Model', 'Cijena', 'Kilometraza', 'Zapremina_motora', 'Snaga_motora', 'Tip', 'Registrovan', 'Godina', 'Gorivo']
            writer.writerow(header)
        else:
            writer = csv.writer(csvfile)

        for i, id in enumerate(ids_to_process):
            article_url = f"{base_url}{id}"
            try:
                response = requests.get(article_url)

                if response.status_code == 200:
                    data = response.json()
                    if data:
                        Brand = data.get('brand', {}).get('name', 'Unknown')
                        Model = data.get('model', {}).get('name', 'Unknown') if data.get('model') else 'Unknown'
                        Cijena = data.get('price', 0)
                        State = data.get('state', 'unknown')

                        attributes = data.get('attributes', [])
                        Kilometraza = next((a.get('value') for a in attributes if a.get('id') == 3), '')
                        Zapremina_motora = next((a.get('value') for a in attributes if a.get('id') == 1144), '')
                        Snaga_motora = next((a.get('value') for a in attributes if a.get('id') == 5), '')
                        Tip = next((a.get('value') for a in attributes if a.get('id') == 59), '')
                        Registrovan = next((a.get('value') for a in attributes if a.get('id') == 6), '0')
                        Godina = next((a.get('value') for a in attributes if a.get('id') == 2), '')
                        Gorivo = next((a.get('value') for a in attributes if a.get('id') == 7), '')

                   

                        if Cijena > 0 and State == 'used':
                            writer.writerow([
                                Brand, Model, Cijena,
                                Kilometraza, Zapremina_motora, Snaga_motora, Tip, Registrovan,
                                Godina, Gorivo, Transmisija
                            ])
                            print(f"Successfully added article id: {id}.")
                        else:
                            print(f"Missing price or new car id: {id}.")
                    else:
                        print(f"Empty response data for article id: {id}.")
                else:
                    print(f"Error fetching article {id}. Status code: {response.status_code}")

            except Exception as e:
                print(f"Exception occurred while fetching article {id}: {e}")

# Pozivanje funkcije sa zadanim parametrima
fetch_article_and_write_to_file("output_unique.txt", "dataset.csv", "2508079", 17050)



def fetch_data_and_write_to_file(url, file_path, start_page, end_page):
    # Učitaj sve postojeće ID-ove iz fajla u set
    existing_ids = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            listing_id = line.strip()
            existing_ids.add(listing_id)

    for page in range(start_page, end_page + 1):
        current_url = f"{url}&page={page}"
        response = requests.get(current_url)

        if response.status_code == 200:
            data = response.json()

            if 'data' in data and isinstance(data['data'], list):
                with open(file_path, 'a', encoding='utf-8') as file:
                    for item in data['data']:
                        listing_id = item.get('id')
                        if listing_id and str(listing_id) not in existing_ids:  # Provjeri da li je ID već u fajlu
                            file.write(f"{listing_id}\n")
                            existing_ids.add(str(listing_id))  # Dodaj ID u set postojećih ID-eva
                        elif not listing_id:
                            print("No 'id' found for this item")

                print(f"Data appended for page {page}")
            else:
                print(f"Invalid JSON structure or missing 'data' key for page {page}")
        else:
            print(f"{current_url} Error fetching data for page {page}. Status code: {response.status_code}")

url = 'https://olx.ba/api/search?&category_id=18&per_page=200'
file_path = 'output.txt'
start_page = 1
end_page = 200
#fetch_data_and_write_to_file(url, file_path, start_page, end_page)

def remove_duplicates_and_sort(input_file, output_file):
    # Čitanje svih brojeva iz output_unique.txt
    try:
        with open(output_file, 'r') as f:
            existing_numbers = set(line.strip() for line in f)
    except FileNotFoundError:
        existing_numbers = set()

    # Čitanje brojeva iz output.txt
    with open(input_file, 'r') as infile:
        for line in infile:
            number = line.strip()
            existing_numbers.add(number)

    # Sortiranje brojeva
    sorted_numbers = sorted(existing_numbers, key=int)

    # Zapisivanje sortirane liste brojeva u output_unique.txt
    with open(output_file, 'w') as outfile:
        for number in sorted_numbers:
            outfile.write(number + '\n')

# Nazivi datoteka
input_file = 'output.txt'
output_file = 'output_unique.txt'

# Poziv funkcije
# remove_duplicates_and_sort(input_file, output_file)




def count_duplicates_from_file(file_path):
    # Čitaj sve linije iz fajla i ukloni praznine i nove redove
    with open(file_path, 'r', encoding='utf-8') as file:
        ids = [line.strip() for line in file]

    # Pretvori stringove u int-ove ako je potrebno
    ids = [int(id) for id in ids]

    # Broji pojavljivanja svakog ID-a u datasetu
    counter = Counter(ids)

    # Filtriraj samo duplikate (one sa više od jednog pojavljivanja)
    duplicates = {key: count for key, count in counter.items() if count > 1}

    return duplicates

# Primer upotrebe funkcije
file_path = 'output.txt'
#duplicates = count_duplicates_from_file(file_path)
#print(duplicates)





def remove_duplicates(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Remove duplicates from sorted list
    unique_lines = []
    previous_line = None

    for line in lines:
        if line != previous_line:
            unique_lines.append(line)
        previous_line = line

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(unique_lines)

# Example usage
file_path = 'output.txt'
#remove_duplicates(file_path)



def sort_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Pretvoriti linije u listu integera i sortirati ih
    sorted_lines = sorted([int(line.strip()) for line in lines if line.strip().isdigit()])

    with open(file_path, 'w', encoding='utf-8') as file:
        for line in sorted_lines:
            file.write(f"{line}\n")

# Primjer upotrebe funkcije za vaš fajl
file_path = 'output_unique.txt'  # Zamijenite sa stvarnom putem do vašeg fajla
#sort_file(file_path)



