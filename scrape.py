import json
from bs4 import BeautifulSoup
from requests_cache import CachedSession
from datetime import timedelta

URL = {'data_penduduk_2019_1':'https://disdukcapil.pesisirbaratkab.go.id/informasi/id/14/data-penduduk-per-desa-sem-i-2019.html',
       'data_penduduk_2019_2':'https://disdukcapil.pesisirbaratkab.go.id/informasi/id/17/data-penduduk-per-desa-sem-2-2019.html',
       'data_penduduk_2020_1':'https://disdukcapil.pesisirbaratkab.go.id/informasi/id/20/data-penduduk-per-desa-sem-1-tahun-2020.html',
       'data_penduduk_2020_2':'https://disdukcapil.pesisirbaratkab.go.id/informasi/id/37/data-penduduk-per-desa-kab--pesisir-barat-sem-ii-tahun-2020.html',
       'data_penduduk_2021_1':'https://disdukcapil.pesisirbaratkab.go.id/informasi/id/50/data-penduduk-per-desa-sem-i--2021.html'
      }


def request():
    session = CachedSession(stale_if_error = True)
    '''
    create response list from URL dict 
    '''
    response_list = []
    for key in URL.keys():
        payload = session.get(URL[key], expire_after = timedelta(days=30))
        response_list.append(payload)
        #print(payload)
    
    # turn response list to html table
    table = []
    for response in response_list:
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        # find all table data tag and put it inside a list
        table.append(soup.find_all('td'))
    
    #print('response from cache:', response.from_cache)
    #print('is response cache expired:', response.is_expired)
    return table


data_2019_1 = request()[0]
data_2019_2 = request()[1]
data_2020_1 = request()[2]
data_2020_2 = request()[3]
data_2021_1 = request()[4]

def extract_data_1(table_content, list_slice):
    # remove hard space 'xa0' character from table
    list_raw = [item.text.replace('\xa0','') for item in table_content][list_slice:]
    #print(list_raw)
    nama_kecamatan = []
    desa_kelurahan = []
    jumlah_pria = []
    jumlah_wanita = []
    kepala_keluarga = []
    jumlah_penduduk = []

    for index, item in enumerate(list_raw):
        #extracting content from list every 6 step
        if index % 6 == 0:
            nama_kecamatan.append(item)
        elif index % 6 == 1:
            desa_kelurahan.append(item)
        elif index % 6 == 2:
            jumlah_pria.append(item)
        elif index % 6 == 3:
            jumlah_wanita.append(item)
        elif index % 6 == 4:
            kepala_keluarga.append(item)
        elif index % 6 == 5:
            jumlah_penduduk.append(item)

    data_raw = {'nama kecamatan':nama_kecamatan[1:],
                'desa kelurahan':desa_kelurahan[1:],
                'jumlah pria':jumlah_pria[1:],
                'jumlah wanita':jumlah_wanita[1:],
                'kepala keluarga':kepala_keluarga[1:],
                'jumlah penduduk':jumlah_penduduk[1:]}
    
    #print(len(jumlah_penduduk))
    #print(jumlah_penduduk)
   
    return data_raw


def extract_data_2(table_content, list_slice):
    # remove hard space 'xa0' character from table
    list_raw = [item.text.replace('\xa0','') for item in table_content][list_slice:]
    #print(list_raw)
    desa_kelurahan = []
    jumlah_pria = []
    jumlah_wanita = []
    kepala_keluarga = []
    jumlah_penduduk = []

    for index, item in enumerate(list_raw):
        #extracting content from list every 6 step
        if index % 5 == 0:
            desa_kelurahan.append(item)
        elif index % 5 == 1:
            jumlah_pria.append(item)
        elif index % 5 == 2:
            jumlah_wanita.append(item)
        elif index % 5 == 3:
            kepala_keluarga.append(item)
        elif index % 5 == 4:
            jumlah_penduduk.append(item)

    data_penduduk = {'desa kelurahan':desa_kelurahan[1:],
                     'jumlah pria':jumlah_pria[1:],
                     'jumlah wanita':jumlah_wanita[1:],
                     'kepala keluarga':kepala_keluarga[1:],
                     'jumlah penduduk':jumlah_penduduk[1:]}
    
    return data_penduduk


data2019_1 = extract_data_1(data_2019_1,list_slice=14)
data2019_2 = extract_data_2(data_2019_2,list_slice=7)
data2020_1 = extract_data_1(data_2020_1,list_slice=10)
data2020_2 = extract_data_2(data_2020_2,list_slice=14)
data2021_1 = extract_data_2(data_2021_1,list_slice=8)

def cleaned_data(raw_data,option):
    if option == 1:
        # for removing - and . in data
        for key, value in raw_data.items():
            if key == 'nama kecamatan' or key == 'desa kelurahan':
                word = [str(line).split('-')[-1] for line in value]
                raw_data[key] = word
            if key in list(['jumlah pria','jumlah wanita','kepala keluarga','jumlah penduduk']):
                word = [str(line).replace('.','') for line in value]
                raw_data[key] = word
    if option == 2:
        # for removing \n and . in data
        for key, value in raw_data.items():
            if key == 'nama kecamatan' or key == 'desa kelurahan':
                word = [str(line).split('\n')[1].split('-')[-1] for line in value]
                raw_data[key] = word
            if key in list(['jumlah pria','jumlah wanita','kepala keluarga','jumlah penduduk']):
                word = [str(line).replace('.','').split('\n')[1] for line in value]
                raw_data[key] = word
        
    return raw_data


cleandata2019_1 = cleaned_data(data2019_1,option=1)
cleandata2019_2 = cleaned_data(data2019_2,option=1)
cleandata2020_1 = cleaned_data(data2020_1,option=2)
cleandata2020_2 = cleaned_data(data2020_2,option=1)
cleandata2021_1 = cleaned_data(data2021_1,option=1)


# function for create json 
def create_json(data, filename,option):
    dump = data
    datain = []
    if option == 1:
        data_length = len(data['nama kecamatan']) - 1
        for index in range(0, data_length):
            insert = {'nama kecamatan': dump['nama kecamatan'][index], 
                      'desa kelurahan': dump['desa kelurahan'][index],
                      'jumlah pria': dump['jumlah pria'][index],
                      'jumlah wanita': dump['jumlah wanita'][index],
                      'kepala keluarga': dump['kepala keluarga'][index],
                      'jumlah penduduk': dump['jumlah penduduk'][index]}
            
            datain.append(insert)

    elif option == 2:
         data_length = len(data['desa kelurahan'])
         for index in range(0, data_length):
            insert = {'desa kelurahan': dump['desa kelurahan'][index],
                      'jumlah pria': dump['jumlah pria'][index],
                      'jumlah wanita': dump['jumlah wanita'][index],
                      'kepala keluarga': dump['kepala keluarga'][index],
                      'jumlah penduduk': dump['jumlah penduduk'][index]}
            
            datain.append(insert)

    with open(filename, 'w') as fp:
        json.dump(datain, fp)
    

create_json(cleandata2019_1, 'data_source/data_penduduk_2019_sem-1.json',option=1)
create_json(cleandata2019_2, 'data_source/data_penduduk_2019_sem-2.json',option=2)
create_json(cleandata2020_1, 'data_source/data_penduduk_2020_sem-1.json',option=1)
create_json(cleandata2020_2, 'data_source/data_penduduk_2020_sem-2.json',option=2)
create_json(cleandata2021_1, 'data_source/data_penduduk_2021_sem-1.json',option=2)
