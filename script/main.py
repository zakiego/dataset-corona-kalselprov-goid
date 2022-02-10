import pandas as pd
import json

file = open("script/list-api.json", 'r')
file = json.load(file)


def get_data(data):
    filename = data["name"] + ".csv"

    # mengambil data dari sebelumnya
    data_before = pd.read_csv(filename)

    # menarik data dari API
    data = pd.read_json(data["url"])

    # dataframe untuk menampung data dari API
    data_new = pd.DataFrame(columns=['tanggal'])

    # ekstrak data dari API
    for index in range(0, len(data)):
        title = data.iloc[index][0]

        content = pd.DataFrame(data.iloc[index][1])
        content = content.rename(columns={0: 'tanggal', 1: title.lower()})

        data_new = pd.merge(data_new, content, on='tanggal', how='outer')

    # menggabungkan dengan data sebelumnya, hapus jika ada baris yang sama
    data_combine = pd.concat([data_before, data_new]
                             ).drop_duplicates().reset_index(drop=True)

    #  mengurutkan berdasarkan tanggal
    data_combine = data_combine.sort_values(
        by=['tanggal'], ascending=[True])

    # save
    data_combine.to_csv(filename, index=False)


for index in range(0, len(file)):
    get_data(file[index])
