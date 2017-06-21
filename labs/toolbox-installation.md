**Toolbox installation**: Installing Atom, Pymakr plugin, Anaconda and others

# Toolbox installation

## Atom
Atom is an Integrated Development Environment (**IDE**), providing convenient features to edit Python code (among many others): syntax highlighting, completion, auto-indentation, integration with Git, bash, ...

We will use Atom to write Python code during the labs sessions. 

To install it, download the installation file for your Operating System here: [https://atom.io/](https://atom.io/)

## Atom | Pymakr plugin
The Python code written will not be executed in your local machine. Instead, you need to transfer it to your IoT device (in our case Pycom Lopy). To do so, [Pycom](https://www.pycom.io/) developed a plugin named **Pymakr** that will facilitate the execution and syncing of Python to the device.

To install the plugin in Atom:

1. Open Atom
2. In top menu: Atom ► Preferences...
3. And write `pymkr` in the input box under the `Install tab` (followed by `Enter`):

![img/install-pymkr.png](http://i.imgur.com/Of2NTPR.png)


## FileZilla
Filezilla will be used occasionnaly to synchronize or retrieve file from IoT device via ftp and Wifi of the device itself.

Download the FileZilla ftp client here: https://filezilla-project.org/


## Anaconda
Python comes in different flavours: different versions and different environment of libraries. Moreover, a Python's version is most probably already installed in your machine. 

So in order to not screw up your installation, it is advised to install Anaconda https://anaconda.org/ which provides a very convenient way to run various Python version with various set of Python modules and libraries in an isolated and safe way.

For our labs, we will use Anaconda version 3.6 https://www.continuum.io/downloads

Once installed (Anaconda with Python version 3.6 by default), we want now to install Python 2.7 as well. To do so:

1. Open `Anaconda Navigator`
2. Click on `Environments` tab
3. Ckick on the arrow on the right of `root` item
4. `Open Terminal`

![img/anaconda-env-prog.png](http://i.imgur.com/Cfp8QSo.png)

Documentation on how setting up various Python versions and environments in Anaconda https://conda.io/docs/py2or3.html

In the terminal:

* to know your current Python version: `python --version`


* to get a list of existing environments: `conda info --envs`

Now, to create a new environment with Python version 2.7:

`conda create -n py4data-2.7 python=2.7 anaconda`

`py4data-2.7` being the name of your environment.


## GitHub Desktop
Git is a version control system (VCS) for tracking changes in computer files and coordinating work on those files among multiple people. 

GitHub is a web-based Git or version control repository facilitating collaborative software development.

We will cover only the very basics of Git during these labs and will use GitHub Desktop standalone.
If you want to have a deeper understanding, you can look at this free online course at Udacity: https://www.udacity.com/course/how-to-use-git-and-github--ud775

So, download it here: https://desktop.github.com/ and install it.

## The Things Network (TTN)
We will use the TTN infrastructure (provided as an online service) to set up a LoRaWan, so log to TTN: https://www.thethingsnetwork.org/ and create an accounte (free). We will use it during the LoRaWan and NanoGateway lab.

