## SQLalchemy  版本迁移工具 alembic 使用

### 安装用到的包

`pip install pymysql`

`pip install sqlalchemy`

`pip install alembic`

### alembic 初始化和配置

完成 pip 安装之后

- 在 shell 里面 cd 到项目根目录执行
  `alembic init alembic `  

- 用 pycharm 把生成的文件 download 回来（包括 `alembic`  目录和 `alembic.ini`）

- 修改 `alembic.ini` 设置数据库连接。 

  > sqlalchemy.url = driver://user:pass@localhost/dbname

- 在 `env.py` 中设置，将target_metadata赋值成数据库的元数据(metadata) 
  如果执行 revision 有 import 报错，注意是否正确将当前项目目录添加到 sys.path 路径

### 基于数据库 model 定义进行更新

将 model 定义好，并确认在 env.py 里导入的 Base 类是在 model 定义的地方的

- 配置完成执行（ -m "注释信息"，根据情况更改，会用到生成的py文件名字里）

  > alembic revision --autogenerate -m "create_user_table"

  这里可以看到虚拟机目录在 alembic/versions 里生成了 py 文件，检查确认更新的内容，然后执行

  > alembic upgrade head

   这样就会更新 mysql 数据库了

### 命令参考

查看记录和历史

> alembic history

查看生成的 py 文件

> ls -l alembic/versions

其他操作

- 删除  alembic/versions/xxx.py 

### 常见问题

#### 执行 alembic 报错，KeyError：'5b29018b55ba'

原因：该版本曾经upgrade执行过了，但是文件被删除，

解决办法：更新数据库 alembic_version 表记录

ERROR [alembic.util.messaging] Can't locate revision identified by 'a2de455a4f51'  FAILED: Can't locate revision identified by 'a2de455a4f51' 

#### 执行 alembic autogenerate 没有看到生成的 py 文件有数据库更新操作的代码

原因：Base import 不正确，或者 model 定义不正确

解决办法：检查 model 代码



### 数据库还没有执行 upgrade head 更新，不能执行 autogenerate

ERROR [alembic.util.messaging] Target database is not up to date.  FAILED: Target database is not up to date. 



### 删除所有 py 文件之后的重新开始，最好把数据库的表也删除完

这样才能确保生成的py文件反应所有数据库变更



### 单独更改列名或一些列属性和表名等不能自动识别

需要注意