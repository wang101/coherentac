import os
import time

#nlst1 = range(1,2)


nlst1 = [0,136,1485,625,832,1125,699,212,606,64,1727,1303,1623,1123,1543,429,521,450,1734,1917,843,1469,691,1246]
nlst1 = [0,136,1485,625]
for i in nlst1:
        newdir = './p'+str(i)+'/'
        pdbname = 'c'+str(i)+'.pdb'
        os.chdir(newdir)
        os.system('cp ../1patt.py .')
        os.system('cp ../qsublow.pbs .')
        os.system('sed -i \'11c python 1patt.py lstc'+str(i)+'.h5\' qsublow.pbs')
        os.system('qsub qsublow.pbs')
        os.chdir('../')


#nlst1 = range(1001,2000,2)
#for i in nlst1:
#        newdir = './p'+str(i)+'/'
#        pdbname = 'c'+str(i)+'.pdb'
#        os.mkdir(newdir)
#        os.chdir(newdir)
#        os.system('cp -r ../root/* .')
#        os.system('cp ' + '../files_pdb/'+ pdbname + ' .')
#        os.system('qsub ./qsubbatch.pbs')
#        os.chdir('../')
#
#while(1):
#    time.sleep(20)
#    if os.system('qstat -u whx | wc -l') == '0':
#        break
#
#print "gen done"
#os.system('mv p*/lstc*.h5 ./files_output/')
#os.system('mv p* ./store/')
#os.chdir('./files_output/')
#os.system('python ave_serial.py')
#os.system('pypython calc_ave.py')
#
