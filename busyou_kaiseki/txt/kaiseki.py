from janome.tokenizer import Tokenizer
import sys, os
from pathlib import Path
import csv, json
import pandas as pd
import glob

fo_names = ['test_txt', 'csv']

for i in fo_names:
    try:
        os.makedirs('../{}'.format(i))
    except:
        continue


file_number = 0
t = Tokenizer()
path = Path(sys.argv[1] if len(sys.argv) >= 2 else '.')
for path_in in [x for x in path.glob('*.txt') if x.is_file()]:
    path_out = path_in.with_suffix('.txt')
    path_csv = path_in.with_suffix('.csv')
    file = open(path_in, 'r')
    file_number += 1
    bunsyou = file.readlines()
    syori_bunsyou = []
    moji = []
    mojisuu = 0

    for i in range(len(bunsyou)):
        bunsyou[i] = bunsyou[i].strip()
        syori_bunsyou.append(bunsyou[i].strip())

    for i in range(len(bunsyou)):
        moji.append(bunsyou[i].split('。'))

    for i in range(len(moji)):
        for j in range(len(moji[i])):
            mojisuu += len(moji[i][j])

    print('{} -> txt/{} ...'.format(path_in, path_out))

    file = open('../test_txt/{}'.format(path_out), 'w')
    file.writelines(syori_bunsyou)

    file = open('../test_txt/{}'.format(path_out), 'r')
    bunseki_bunsyou = file.read()
    bunseki_bunsyou = bunseki_bunsyou.replace('\u3000', '')
    bunseki_bunsyou = bunseki_bunsyou.replace('  ', '')
    bunseki_bunsyou = bunseki_bunsyou.replace(' ', '')
    bunseki_bunsyou = bunseki_bunsyou.replace('href', '')
    bunseki_bunsyou = bunseki_bunsyou.replace('="', '')
    bunseki_bunsyou = bunseki_bunsyou.replace('://', '')
    bunseki_bunsyou = bunseki_bunsyou.replace('https', '')
    bunseki_bunsyou = bunseki_bunsyou.replace('syosetu', '')
    bunseki_bunsyou = bunseki_bunsyou.replace('com', '')
    bunseki_bunsyou = bunseki_bunsyou.replace('/', '')
    bunseki_bunsyou = bunseki_bunsyou.replace('/">', '')
    bunseki_bunsyou = bunseki_bunsyou.replace('ncode', '')
    bunseki_bunsyou = bunseki_bunsyou.replace('9227', '')
    bunseki_bunsyou = bunseki_bunsyou.replace('n', '')
    bunseki_bunsyou = bunseki_bunsyou.replace('er', '')
    bunseki_bunsyou = bunseki_bunsyou.replace('～</', '')


    name_list = []
    hon_list = {}

    for token in t.tokenize(bunseki_bunsyou):
        if (token.surface not in name_list):
            name_list.append(token.surface)
            hon_list['{}'.format(token.surface)] = 1
        else:
            hon_list[token.surface] += 1

    hinsi_list = sorted(hon_list.items(), key=lambda x: -x[1])

    hinsi_name = []
    hinsi_dict = {}
    for i in range(len(hinsi_list)):
        token = t.tokenize(hinsi_list[i][0])[0]
        bunrui = token.part_of_speech.split(',')
        if ('{} {}'.format(bunrui[0], bunrui[1]) not in hinsi_name):
            hinsi_name.append('{} {}'.format(bunrui[0], bunrui[1]))
            hinsi_dict['{} {}'.format(bunrui[0], bunrui[1])] = hinsi_list[i][1]
        else:
            hinsi_dict['{} {}'.format(bunrui[0], bunrui[1])] += hinsi_list[i][1]

    hinsi_dict['文字数'] = mojisuu
    to_hinsi_list = sorted(hinsi_dict.items(), key=lambda x: -x[1])

    print('{} -> csv/{} ...'.format(path_in, path_csv))

    with open('../csv/{}'.format(path_csv), 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(to_hinsi_list)

csv_files = [os.path.basename(r) for r in glob.glob('../csv/*.csv')]

list1 = []

for f in csv_files:
    try:
        list1.append(pd.read_csv('../csv/{}'.format(f), encoding='shift-jis', header=None, index_col=0, engine='python'))
    except:
        continue

df = pd.concat(list1, axis=1)
df = df.fillna(0)

print('全てのCSVファイルをTOTAL.csvに統合しました')
df.to_csv('../csv/TOTAL.csv', encoding='shift-jis', header=False)
