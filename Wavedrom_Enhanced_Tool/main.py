#libraries
import pandas as pd
#read csv file and transit the data
wave = pd.read_csv('wave.csv',header=None, dtype=object)
wave = wave.T

#items are all the elements in the data
items = wave.columns
wave_length = 0
dic_items = {}                  #colect all  items
dic_setting = {'edge':[]}       #colect all ! start non-length items

#get the wave length first
for i in items:
    if wave[i][0] == '!length':
        for end_find in wave[i][1:]:
            wave_length += 1
            if end_find == 'end':
                break    
        print ('[INFO] wave length is:',wave_length)
        break

for i in items:
    if wave[i][0][0] == '!':            #get ! start non-length items
        if wave[i][0][1:] == 'edge':    #get edge
            dic_setting['edge'].append(wave[i][1:3].to_list())
            print('[INFO] edge :',wave[i][1:3].to_list())
    else:      
        dic_items[wave[i][0]] = wave[i][1:wave_length+1].fillna('.').to_list()

        print('[INFO]',wave[i][0],' :',dic_items[wave[i][0]])

js_name = []#name
js_wave = []#wave
js_data = []#data
js_node = []#node

for i in dic_items:
    js_name.append(i)
    wave_e = ''
    data_e = ''
    node_e = ''
    for e in dic_items[i]:
        info_list = e.split(',')
        if (len(info_list) == 3):
            wave_e = wave_e + info_list[0]
            data_e = data_e + '\'' + info_list[1] + '\','
            node_e = node_e + info_list[2]
        else:
            wave_e = wave_e + e
            node_e = node_e + '.'

    js_wave.append(wave_e)
    js_data.append(data_e)
    js_node.append(node_e)   

#write and save js file
file = open('wave.js','w')

file.write('{signal:[\n')
for i in range(len(js_name)):#write signals
    file.write('\t{name:\'')
    file.write(js_name[i])
    file.write('\',wave:\'')
    file.write(js_wave[i])
    file.write('\',data:[')
    file.write(js_data[i])
    file.write('],node:\'')
    file.write(js_node[i])
    file.write('\'},\n')
file.write('],')
file.write('edge:[\n')

for i in dic_setting['edge']:#write other items - edge
    file.write('\'')
    file.write(i[0])
    file.write(' ')
    file.write(i[1])
    file.write('\',\n')
file.write(']}')

file.close()