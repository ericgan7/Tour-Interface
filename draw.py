
import csv
import os
import random

class draw(object):
    def __init__(self):
        '''
        self.pfile = 'OUTPUT_PARAMETERS.csv'
        self.outp_file = open(self.pfile, 'w', newline = '')
        self.outp = csv.writer(self.outp_file, delimiter = ',')
        self.outp.writerow(["TOURSET", "DISTRIBUTIONS 0.2", "DISTRIBUTIONS 0.3", None, 
                             "ALPHA", "BETA", "GAMMA", None, 
                             "RANDOM", "DELTA 0.2", "DELTA 0.3", None])
        
        self.dfile = 'OUTPUT_DRAW.csv'
        self.outd_file = open(self.dfile, 'w', newline= '')
        self.outd = csv.writer(self.outd_file, delimiter = ',')
        self.outd.writerow(["TOUR ID", "DELTA", None])
        '''

        self.tourset = None
        self.input_file = None
        self.input = None
        
        self.zero = ['0','0','0']
        self.params = []
        self.dist = []
        self.tour = []
        self.d = 0

        self.parameters = [["TOURSET", "DISTRIBUTIONS", None,
                             "ALPHA", "BETA", "GAMMA", None, 
                             "RANDOM", "DELTA", None]]
        self.data = [["TOUR ID", "DELTA", None]]
        
    def run(self, tourID, delta):
        isParam = True
        length = 0
        for i, row in enumerate(self.input_file):
            result = row.strip().split(',');
            if i == 0:
                length = len(result) - 5
                for x in range(length):
                    self.tour.append([])
            if (result[-5:-2] == self.zero):
                if i == 0:
                    return
                else:
                    isParam = False
            if (isParam):
                self.params.append([result[-5], result[-4], result[-3]])
                self.dist.append([result[-2], result[-1]])
            for i in range(length):
                self.tour[i].append(result[i])
            
        index = self.random(delta)
        self.parameters.append([tourID] + self.dist[self.d] + [None] + self.params[0] + [None, index, self.d, None])
        for i, row in enumerate(self.params):
            if i == 0:
                continue
            self.parameters.append([None] + self.dist[i] + [None] + self.params[i])
        self.parameters.append([])
        try:
            self.data.append([tourID, delta] + self.tour[self.d])
        except IndexError:
            import pdb; pdb.set_trace()
        self.data.append([])
            
    def random(self, delta):
        index = random.random()
        total = 0
        delta_index = 0
        if (delta == '0.2'):
            delta_index = 0
        else:
            delta_index = 1
        for i, d in enumerate(self.dist):
            total += float(d[delta_index])
            if total >= index:
                self.d = i
                break
        total = 0
        return index
        
    def new(self, file, delta):
        random.seed()
        self.tourset = file + '.csv'
        self.input_file = open(self.tourset, 'r', newline = '')
        self.input = csv.reader(self.input_file, delimiter = ',')
        
        self.params = []
        self.input = []
        self.tour = []
        self.dist = []

    def reset(self):
        self.parameters = [["TOURSET", "DISTRIBUTIONS 0.2", "DISTRIBUTIONS 0.3", None, 
                             "ALPHA", "BETA", "GAMMA", None, 
                             "RANDOM", "DELTA " + delta, None]]
        self.data = [["TOUR ID", "DELTA", None]]

    def write(self, type, name, directory):
        if name[-4:] != '.csv':
            name = name + '.csv'
        import pdb; pdb.set_trace()
        with open(os.path.join(directory, name), 'w', newline = '') as stream:
            output = csv.writer(stream, delimiter = ',')
            if type == 'DATA':
                for row in self.data:
                    output.writerow(row)
            elif type == "PARAM":
                for row in self.parameters:
                    output.writerow(row)
            stream.close()


        