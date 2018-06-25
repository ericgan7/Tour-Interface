
import csv
import random

class draw(object):
    def __init__(self):
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
        
        self.tourset = None
        self.input_file = None
        self.input = None
        
        self.zero = ['0','0','0']
        self.params = []
        self.dist = []
        self.tour = []
        self.d2 = 0
        self.d3 = 0
        
        
    def run(self, tourID):
        #import pdb; pdb.set_trace()
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
            
        index = self.random()
        try:
            self.outp.writerow([tourID] + self.dist[0] + [None] + self.params[0] + [None, index, self.d2, self.d3, None])
        except IndexError:
            import pdb; pdb.set_trace()
        for i, row in enumerate(self.params):
            if i == 0:
                continue
            self.outp.writerow([None] + self.dist[i] + [None] + self.params[i])
        self.outp.writerow([])
        
        self.outd.writerow([tourID, '0.2'] + self.tour[self.d2])
        self.outd.writerow([None, '0.3'] + self.tour[self.d3])
        self.outd.writerow([])
            
    def random(self):
        index = random.random()
        total = 0
        for i, d in enumerate(self.dist):
            total += float(d[0])
            if total >= index:
                self.d2 = i
                break
        total = 0
        for i, d in enumerate(self.dist):
            total += float(d[1])
            if total >= index:
                self.d3 = i
                break
        return index
    
    def end(self):
        self.input_file.close()
        self.outp_file.close()
        self.outd_file.close()
        print("DONE")
        
    def new(self, file, tourid):
        random.seed()
        self.tourset = file + '.csv'
        self.input_file = open(self.tourset, 'r', newline = '')
        self.input = csv.reader(self.input_file, delimiter = ',')
        
        self.params = []
        self.input = []
        self.tour = []
        
        self.run(tourid)
        