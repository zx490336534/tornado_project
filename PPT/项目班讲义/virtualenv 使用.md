## virtualenv

[virtualenv](http://pypi.python.org/pypi/virtualenv) 是一个创建隔绝的Python环境的 工具。virtualenv创建一个包含所有必要的可执行文件的文件夹，用来使用Python工程所需的包。

它可以独立使用，代替Pipenv。

通过pip安装virtualenv：

```
$ pip install virtualenv
```

测试您的安装

```
$ virtualenv --version
```

### 基本使用

1. 为一个工程创建一个虚拟环境：

```
$ cd my_project_folder
$ virtualenv my_project
```

`virtualenv my_project` 将会在当前的目录中创建一个文件夹，包含了Python可执行文件， 以及 `pip` 库的一份拷贝，这样就能安装其他包了。虚拟环境的名字（此例中是 `my_project` ） 可以是任意的；若省略名字将会把文件均放在当前目录。

在任何您运行命令的目录中，这会创建Python的拷贝，并将之放在叫做 [:file:`my_project`](https://github.com/Prodesire/Python-Guide-CN/blob/master/docs/dev/virtualenvs.rst#id13) 的文件中。

您可以选择使用一个Python解释器（比如``python2.7``）：

```
$ virtualenv -p /usr/bin/python2.7 my_project
```

或者使用``~/.bashrc``的一个环境变量将解释器改为全局性的：

```
$ export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python2.7
```

1. 要开始使用虚拟环境，其需要被激活：

```
$ source my_project/bin/activate
```

当前虚拟环境的名字会显示在提示符左侧（比如说 `(my_project)您的电脑:您的工程 用户名$） 以让您知道它是激活的。从现在起，任何您使用pip安装的包将会放在 ``my_project` 文件夹中， 与全局安装的Python隔绝开。

像平常一样安装包，比如：

```
$ pip install requests
```

1. 如果您在虚拟环境中暂时完成了工作，则可以停用它：

```
$ deactivate
```

这将会回到系统默认的Python解释器，包括已安装的库也会回到默认的。

要删除一个虚拟环境，只需删除它的文件夹。（要这么做请执行 `rm -rf my_project` ）

然后一段时间后，您可能会有很多个虚拟环境散落在系统各处，您将有可能忘记它们的名字或者位置。

### 其他注意

运行带 `--no-site-packages` 选项的 `virtualenv` 将不会包括全局安装的包。 这可用于保持包列表干净，以防以后需要访问它。（这在 `virtualenv` 1.7及之后是默认行为）

为了保持您的环境的一致性，“冷冻住（freeze）”环境包当前的状态是个好主意。要这么做，请运行：

```
$ pip freeze > requirements.txt
```

这将会创建一个 [:file:`requirements.txt`](https://github.com/Prodesire/Python-Guide-CN/blob/master/docs/dev/virtualenvs.rst#id16) 文件，其中包含了当前环境中所有包及 各自的版本的简单列表。您可以使用 “pip list”在不产生requirements文件的情况下， 查看已安装包的列表。这将会使另一个不同的开发者（或者是您，如果您需要重新创建这样的环境） 在以后安装相同版本的相同包变得容易。

```
$ pip install -r requirements.txt
```

这能帮助确保安装、部署和开发者之间的一致性。

最后，记住在源码版本控制中排除掉虚拟环境文件夹，可在ignore的列表中加上它。 （查看 [:ref:`版本控制忽略`](https://github.com/Prodesire/Python-Guide-CN/blob/master/docs/dev/virtualenvs.rst#id18)）

## virtualenvwrapper

[virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/index.html) 提供了一系列命令使得和虚拟环境工作变得愉快许多。它把您所有的虚拟环境都放在一个地方。

安装（确保 **virtualenv** 已经安装了）：

```
$ pip install virtualenvwrapper
$ export WORKON_HOME=~/Envs
$ source /usr/local/bin/virtualenvwrapper.sh
```

([virtualenvwrapper 的完整安装指引](https://virtualenvwrapper.readthedocs.io/en/latest/install.html).)

对于Windows，您可以使用 [virtualenvwrapper-win](https://github.com/davidmarble/virtualenvwrapper-win/) 。

安装（确保 **virtualenv** 已经安装了）：

```
$ pip install virtualenvwrapper-win
```

在Windows中，WORKON_HOME默认的路径是 %USERPROFILE%Envs 。

### 基本使用

1. 创建一个虚拟环境：

```
$ mkvirtualenv my_project
```

这会在 [:file:`~/Envs`](https://github.com/Prodesire/Python-Guide-CN/blob/master/docs/dev/virtualenvs.rst#id23) 中创建 [:file:`my_project`](https://github.com/Prodesire/Python-Guide-CN/blob/master/docs/dev/virtualenvs.rst#id25) 文件夹。

1. 在虚拟环境上工作：

```
$ workon my_project
```

或者，您可以创建一个项目，它会创建虚拟环境，并在 `$WORKON_HOME` 中创建一个项目目录。 当您使用 `workon myproject`时，会 `cd` -ed 到项目目录中。

```
$ mkproject myproject
```

**virtualenvwrapper** 提供环境名字的tab补全功能。当您有很多环境， 并且很难记住它们的名字时，这就显得很有用。

`workon` 也能停止您当前所在的环境，所以您可以在环境之间快速的切换。

1. 停止是一样的：

```
$ deactivate
```

1. 删除：

```
$ rmvirtualenv my_project
```

### 其他有用的命令

- `lsvirtualenv`

  列举所有的环境。

- `cdvirtualenv`

  导航到当前激活的虚拟环境的目录中，比如说这样您就能够浏览它的 [:file:`site-packages`](https://github.com/Prodesire/Python-Guide-CN/blob/master/docs/dev/virtualenvs.rst#id28) 。

- `cdsitepackages`

  和上面的类似，但是是直接进入到 [:file:`site-packages`](https://github.com/Prodesire/Python-Guide-CN/blob/master/docs/dev/virtualenvs.rst#id30) 目录中。

- `lssitepackages`

  显示 [:file:`site-packages`](https://github.com/Prodesire/Python-Guide-CN/blob/master/docs/dev/virtualenvs.rst#id32) 目录中的内容。

[virtualenvwrapper 命令的完全列表](https://virtualenvwrapper.readthedocs.io/en/latest/command_ref.html) 。







## pip douban 源

[pip使用豆瓣的镜像源](https://www.cnblogs.com/ZhangRuoXu/p/6370107.html)



http://pypi.douban.com/simple/
注意后面要有/simple目录。
使用镜像源很简单，用-i指定就行了：


sudo easy_install -i http://pypi.douban.com/simple/ ipython
sudo pip install -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com/simple ipython
每次都要这样写？ no！，做个别名吧，额，类似于这样

pip install -ihttps://pypi.doubanio.com/simple/--trusted-host pypi.doubanio.com django
好像还不太好，肿么办？写在配置文件里吧。
	1. 
linux/mac用户将它命名为pip.conf, windows用户将它命名为pip.ini. 文件中写如下内容:
[global]timeout = 60
index-url = https://pypi.doubanio.com/simple

** 注意： **如果使用http链接，需要指定trusted-host参数

[global]timeout = 60
index-url = http://pypi.douban.com/simple
trusted-host = pypi.douban.com


	1. 
将该文件放置在指定位置.


linux下指定位置为
$HOME/.config/pip/pip.conf
或者
$HOME/.pip/pip.conf
mac下指定位置为
$HOME/Library/Application Support/pip/pip.conf
或者
$HOME/.pip/pip.conf
windows下指定位置为
%APPDATA%\pip\pip.ini
或者
%HOME%\pip\pip.ini