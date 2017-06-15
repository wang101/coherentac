import os
import time

#nlst1 = range(1,2)

n_proc = 40
n_angles = 5000
work_per_proc = int(n_angles/n_proc)
nlst1 = [0,136,1485,625]
for i in nlst1:
        newdir = './p'+str(i)+'/'
        pdbname = 'c'+str(i)+'.pdb'
        os.mkdir(newdir)
        os.chdir(newdir)
        for n in range(n_proc):
            newdir2 = './p'+str(n)+'/'
            os.mkdir(newdir2)
            os.chdir(newdir2)
            os.system('cp -r ../../root/* .')
            os.system('cp ../../files_pdb/'+ pdbname + ' .')
            os.system('sed -i \'2c protein_file='+pdbname+'\' task.input')
            start1 = 36
            stop1 = work_per_proc*n + start1 - 1
            start2 = stop1 + work_per_proc + 1
            stop2 = n_angles + start1 - 1
            if n != n_proc:
                os.system('sed -i \'%d,%dd\' ./task.input'%(start2,stop2))
            if n != 0:
                os.system('sed -i \'%d,%dd\' ./task.input'%(start1,stop1))
            os.system('qsub ./qsublow.pbs')
            os.chdir('../')
        os.chdir('../')


#nlst1 = range(1001,2000,2)
#for i in nlst1:
#        newdir = './p'+str(i)+'/'
#        pdbname = 'c'+str(i)+'.pdb'
#        os.mkdir(newdir)
#        os.chdir(newdir)
#        os.system('cp -r ../root/* .')
#        os.system('cp ' + '../files_pdb/'+ pdbname + ' .')
#        os.system('sed -i \'5c protein_file='+pdbname+'\' task.input')
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
