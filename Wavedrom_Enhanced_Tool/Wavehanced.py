#libraries
import pandas as pd
#read csv file and transit the data
wave_file = pd.read_csv('wave.csv',header=None, dtype=object)
wave = wave_file.T

#items are all the elements in the data
items = wave.columns
wave_length = 0

#get the wave length first
for i in items:
    if wave[i][0] == '!length':
        for end_find in wave[i][1:]:
            wave_length += 1
            if end_find == 'end':
                break    
        print ('[INFO] wave length is:',wave_length)
        break

#WAVE LENGTH

#wave_length
wave_line_dic = {'name':'','wave':'','data':[],'node':''}
dic = {'signal':[],'edge':[]}
line_pointer = 0

for i in items:
    line_flag = False

    if wave[i][0][0] == '!':
        #get ! start key words items

        if wave[i][0][1:] == 'edge':
            edge_element = wave[i][1:wave_length+1].dropna().to_list()
            dic['edge'].append(edge_element)
            print('[INFO] edge :',edge_element)

        elif wave[i][0][1:] == 'data':
             data_element = wave[i][1:wave_length+1].dropna().to_list()
             dic['signal'][line_pointer-1]['data'] = data_element
             print('[INFO] data :',data_element)
        
        elif wave[i][0][1:] == 'node':
             node_element = ''.join(wave[i][1:wave_length+1].fillna('.').to_list())
             dic['signal'][line_pointer-1]['node'] = node_element
             print('[INFO] node :',node_element)
    else:
        line_pointer += 1
        line_flag = True
        wave_line_dic = {'name':'','wave':'','data':[],'node':''}

        wave_line_name = wave[i][0]      
        wave_line_wave = ''.join(wave[i][1:wave_length+1].fillna('.').to_list())

        wave_line_dic['name'] = wave_line_name
        wave_line_dic['wave'] = wave_line_wave

        print('[INFO]',wave_line_name,' :',wave_line_wave)

    if line_flag == True:
        dic['signal'].append(wave_line_dic)

  

#write and save js file
file = open('wave.js','w')

file.write('{signal:[\n')
for wave_line in dic['signal']:
    #write signals
    file.write('\t{name:\'')
    file.write(wave_line['name'])
    file.write('\',wave:\'')
    file.write(wave_line['wave'])
    file.write('\',data:[')

    for blk_name in wave_line['data']:
        file.write('\'')
        file.write(blk_name)
        file.write('\',')

    file.write('],node:\'')
    file.write(wave_line['node'])
    file.write('\'},\n')
file.write('],')

file.write('edge:[\n')

for edge_line in dic['edge']:
    #write other items - edge
    file.write('\'')
    file.write(edge_line[0])
    file.write(' ')
    file.write(edge_line[1])
    file.write('\',\n')
file.write(']}')

file.close()