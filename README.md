# vertical_federated_learning

###
master 本地版本

###
remote 远程版本


##文件目录

   |--Servers<br>
   |   |--utils<br>
   |   |   |--__init__.py<br>
   |   |   |--funct.py 								 # SERVER的工具函数<br>
   |   |--ServerC<br>
   |   |   |--log.log 									# 服务日志<br>
   |   |   |--ServerC.py							  # SERVERC 服务 <br>
   |   |   |--__init__.py<br>
   |   |--__init__.py<br>
   |   |--entity<br>
   |   |   |--__init__.py<br>
   |   |   |--data_type.py 						 # PublicKey EncryptedArray 类<br>
   |   |--ServerA<br>
   |   |   |--log.log  									# 服务日志<br>
   |   |   |--ServerA.py 							  # SERVERA 服务<br> 
   |   |   |--__init__.py<br>
   |--Clinets<br>
   |   |--utils<br>
   |   |   |--__init__.py<br>
   |   |   |--utils.py  								   # 加载测试数据<br>
   |   |--ClinetA<br>
   |   |   |--__init__.py<br>
   |   |   |--ClientA.py								# ClinetA 类<br>
   |   |   |--main.py									# ClinetA 训练代码<br>
   |   |--ClientB<br>
   |   |   |--ClientB.py								# ClinetB 类<br>
   |   |   |--__init__.py<br>
   |   |   |--main.py									# ClinetB 训练代码<br>
   |   |--__init__.py<br>
   |   |--entity<br>
   |   |   |--Client.py<br>
   |   |   |--DataType.py							 # Clinet类里的数据<br>
   |   |   |--__init__.py<br>
   |   |--main.py							 			  # 开两个线程跑训练A和训练B的代码<br>
