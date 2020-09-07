# vertical_federated_learning

###
master 本地版本

###
remote 远程版本


##文件目录

   |--Servers<br>
   |   |--utils<br>
   |   |   |--__init__.py
   |   |   |--funct.py<br> 								 # SERVER的工具函数<br>
   |   |--ServerC
   |   |   |--log.log 									# 服务日志
   |   |   |--ServerC.py							  # SERVERC 服务 
   |   |   |--__init__.py
   |   |--__init__.py
   |   |--entity
   |   |   |--__init__.py
   |   |   |--data_type.py 						 # PublicKey EncryptedArray 类
   |   |--ServerA
   |   |   |--log.log  									# 服务日志
   |   |   |--ServerA.py 							  # SERVERA 服务 
   |   |   |--__init__.py
   |--Clinets
   |   |--utils
   |   |   |--__init__.py
   |   |   |--utils.py  								   # 加载测试数据
   |   |--ClinetA
   |   |   |--__init__.py
   |   |   |--ClientA.py								# ClinetA 类
   |   |   |--main.py									# ClinetA 训练代码
   |   |--ClientB
   |   |   |--ClientB.py								# ClinetB 类
   |   |   |--__init__.py
   |   |   |--main.py									# ClinetB 训练代码
   |   |--__init__.py
   |   |--entity
   |   |   |--Client.py
   |   |   |--DataType.py							 # Clinet类里的数据
   |   |   |--__init__.py
   |   |--main.py							 			  # 开两个线程跑训练A和训练B的代码
