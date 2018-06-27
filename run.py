import draw

d = draw.draw()

def file_range(file, start, end, delta):
    for i in range(start, end):
        print(file + str(i))
        d.new(file + str(i), delta)
        d.run(i, delta)
    
def file_single(file):
    d.new(file, 1)

file = 'tourset'
start = 1
end = 5

file_range(file, start, end, delta = '0.2')
