Generate Auto-correlation (Fast mode)

* 设定角度
```
	cd root
	vim task.input
	#在这里， 将RAND_EULER设为ON，并删除angle打头的所有行
	#将rand_euler_num设为你想要的角度（orientation）的个数
	python init.py
	#会生成一个 task 文件，将 task 文件第三行之后的复制粘贴到task.input 中
	#注意格式为：angle=角度1，角度2，角度3
	#在task.input中，将RAND_EULER设为OFF
	cd ..
```

* 开始模拟
		将file_pdb拷贝或链接到目录下（root的父目录）
		调整模拟选项：修改`jobfast.py`文件。
		其中`n_proc`是每一个complex的CPU核数
		`n_angles`是每一个complex的orientation的数目，最好是`n_proc`的整倍数。
		`start1`是task.input 中angle行起始的行号 (一般不需修改)
		`nlst1`是complex的标号集合，例如，计算`c0.pdb`、`c136.pdb`、`c1485.pdb`、`c625.pdb`则： nlst1 = [0,136,1485,625]
		运行则产生pm/pn/ 目录。 其中m是complex 编号，n是运行批次，n最大为`n_proc`
```
	python jobfast.py
```

* 整理模拟结果
```
	#以complex0:c0.pdb 为例
	cd p0 
	mkdir s
	mv p*/s/* ./s/     #这个p*是在p0的子目录下
	cp ../fitangle.py .
	cp ./p0/task.input .
	python fitangle.py
	#这一步之后会生成lstc0.h5文件，包含所有以复数形式储存的散射图复振幅。
```
		
* 生成相干图
修改`1patt.py`文件中的`shift`（平移量）、 `inds`（干涉所用的orientation的编号）、coherent的参数。
这里为了使得coherent和 noncoherent的数据有可比性，两个数据使用的平移量都一致，编号都是按一定规律生成的。
coherent函数定义：coherent(相干粒子数, orientation数, 散射图文件名)。文件名默认以命令行参数形式传入，方便`jobcoherent.py`调用。
修改`jobcoherent.py`文件中的`nlst1`，应和`jobfast.py`中一致。
```
	python jobcoherent.py
```
运行此命令后，会在p0 （以及其他nlst1中的complex）目录下生成类似`10co_lstc0.h5`。其中10代表10个粒子干涉，co代表相干，no代表不相干，0代表complex编号。

* 生成Auto correlation
```
#在根目录下建立的ac文件夹作为计算Autocorrelation的工作目录
cd ac
#将刚才生成的所有相干图放在data目录下
mkdir data && cd data
cp ../../p*/*o_lstc*.h5 .
# 修改qsublow.pbs 中 ppn 和 最后一行最后一个参数 为使用的CPU核数
vim qsublow.pbs
qsub qsublow.pbs
```
运行完毕之后，会在ac目录下产生`h5corr`文件夹，文件夹中包括所有的autocorrelation 文件。建议按类整理：
```
# 按类整理，如5co是5个粒子相干叠加的文件
cd h5corr
mkdir 5co
mv 5co_lstc* ./5co
```
画图，移动到`ac`目录下。
修改`draw.py`参数，`hstd`是比较标准，h1是对比的coherent，h2是对比的non-coherent。运行`draw.py`会做出相关系数关于对比个数的关系图。蓝色为coherent，绿色为non-coherent。

		
		