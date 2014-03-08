import pickle

file=open('pratikgmaildump.txt','r')
emails1 = pickle.load(file)
file.close()
emails = filter(lambda x: x['From'].find('root@localhost')==-1, emails1)

