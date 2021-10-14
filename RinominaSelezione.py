import requests
from bs4 import BeautifulSoup
from num2words import num2words
from os import listdir, rename
from os.path import isfile, join, splitext, exists

class_name = 'wikitable'
base_url = 'https://it.wikipedia.org/wiki'
it_key = 'Titolo italiano'
en_key = 'Titolo originale'


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def number_to_ordinal(number: int):
    string = num2words(number, to='ordinal', lang='it')
    return string[:-1] + 'a'


def get_url(tv_series: str, season_no: int):
    tv_series = tv_series.replace(' ', '_')
    season_no = number_to_ordinal(season_no)
    preposition = 'de' if tv_series[0].lower() == 'i' else 'di'

    url = f'{base_url}/Episodi_{preposition}_{tv_series}_({season_no}_stagione)'

    if requests.get(url).status_code == 200:
        return url

    url = input(f'Inserisci l\'URL della pagina Wikipedia contenente gli episodi di {tv_series}: ')

    if requests.get(url).status_code == 200:
        return url

    return None


def get_data(url: str):
    wiki_page = requests.get(url)
    if wiki_page.status_code != 200:
        return []

    soup = BeautifulSoup(wiki_page.content, 'html.parser')

    table = soup.find('table', class_=class_name)
    headers = [header.find(text=True).strip() for header in table.find_all('th')]
    results = [{ headers[i]: cell.text.strip() for i, cell in enumerate(row.find_all('td')) } for row in table.find_all('tr')]

    if len(results) > 0:
        del results[0] # delete header row

    return results


def format_title(tv_series: str, season_no: int, titles: dict, extension: str):
    episode_no = titles['no'].zfill(2)
    it_title = titles['it']
    en_title = titles['en']

    return f'{tv_series}. {season_no}x{episode_no} {it_title} - {en_title}{extension}'


def rename_file(src: str, dst: str):
    try:
        rename(src, dst)
        return True
    except WindowsError as e:
        print(str(e))
        return False


if __name__ == '__main__':
    # input directory files path to rename
    absolute_path = input('Inserisci il percorso assoluto dei file da rinominare: ')

    assert exists(absolute_path), 'Percorso specificato non trovato!'

    files = [file for file in listdir(absolute_path) if isfile(join(absolute_path, file))]

    # input TV series & season number
    tv_series = input('Serie tv: ')
    season_no = input('Stagione: ')

    assert season_no.isdigit(), 'Attenzione, stagione deve essere un valore numerico!'

    season_no = int(season_no)

    # get URL
    url = get_url(tv_series, season_no)

    assert url is not None, 'URL errato.'

    # get data
    rows = get_data(url)

    # confirm new filenames
    renames = []

    for index, file in enumerate(files):
        _, extension = splitext(file)

        if index >= len(rows):
            break

        titles = {
            'no': str(index + 1),
            'it': rows[index][it_key] if it_key in rows[index] else rows[index][en_key],
            'en': rows[index][en_key]
        }

        title = format_title(tv_series, season_no, titles, extension)
        src = join(absolute_path, file)
        dst = f'{absolute_path}\\{title}'

        renames.append([src, dst])

        print(f'{bcolors.ENDC}{file} > {bcolors.BOLD}{title}{bcolors.ENDC}')

    confirm = input('Confermi (Y/n)? ')

    if confirm.lower() != 'y':
        exit()

    # rename files
    renamed_files = 0

    for index, rename_list in enumerate(renames):
        src, dst = rename_list

        if rename_file(src, dst):
            renamed_files += 1
        else:
            print(f'{bcolors.FAIL}Errore file n. {index + 1}.\t{src}{bcolors.ENDC}')

    print(f'\n\n{bcolors.UNDERLINE}{renamed_files} file rinominati.{bcolors.ENDC}')
