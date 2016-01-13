from trainFiles import makeTrainFile, mergeDollarAndOilCurs, updateTrainFile
from netManagement import createAndTrainNetwork, trainNetwork, loadNet


def makeNet():
    net_error = 10
    tries = 0
    while net_error > 0.2:
        train_result = createAndTrainNetwork(merged_curs_filename, 6, count_samples, net_filename)
        print train_result
        net_error = train_result[0][0][-1]
        tries += 1
    print tries
    print net_error
    return train_result[-1]


input_list_length = 5
count_samples = 60
curs_filename = 'new_sample.xlsx'
oil_filename = 'BRN_141224_151231.csv'
merged_curs_filename = 'new_sample_with_oil.xlsx'
curs_data_for_proc = [71.2553, 71.1211, 70.9333, 69.5165]
curs_data_oil_for_proc = [70.9333, 69.5165, 70.2690, 70.2690, 37.61, 37.61]
new_curs = [70.2690, 70.7865, 72.5066, 72.8827, 37.12, 36.59]
net_filename = 'net_curs_dollar_with_oil.xml'
#makeTrainFile(curs_filename, count_samples, input_list_length)
#mergeDollarAndOilCurs(curs_filename, oil_filename, merged_curs_filename, count_samples, input_list_length, 2)
net_filename = makeNet()
#first = 'net_curs_dollar_with_oil0.157988685995.xml'
net = loadNet(net_filename)
#test_list = list(input('Input data:'))
result = net.activate(new_curs)
print result





