**GitHub introduction**: an insanely short introduction to Github.

# GitHub introduction

## Introduction
Covering Git and Github would deserve several days. In this lab. we will simply illustrate some typical Git/GitHub workflows using:

* a GitHub account
* and GitHub desktop.


## Learning outcomes

You will learn how to:
* create a GitHub account
* how to collaborate on a common programming project
* how to push/pull changes
* how to fix conflictual changes
* how to create and work on topic branches

## Required Components

For this example you will need:

- a GitHub account
- a development PC


## 1. Workflow


**Step 1: Team leader creates a common GitHub repository**

Repo. url: https://github.com/franckalbinet/ictp-smr-3128-gh-intro

**Step 2: Team members create a GitHub account**

https://github.com/ (free of charge)

**Step 3: Team members Install GitHub desktop**
 
[Please refer to toolbox-installation.md](toolbox-installation.md)

**Step 4: Team members clone the common repo.**

Cloning url: `git@github.com:franckalbinet/ictp-smr-3128-gh-intro.git`

In top menu ► File ► Clone Repository...

Paste the url  of the repository you want to clone and specify the local path where you want to save it.

And clone it...

![img/github-desktop-cloning.png](http://i.imgur.com/LkM6asK.png)

**Step 5: Team members create a new file**

File name should follow the convention: `groupname.md`

**Step 6: Team members push it (it fails)**

**Step 7: Team leader adds them as collaborators**

![img/gh-add-collab.png](http://i.imgur.com/mNWGOp7.png)

**Step 8: Team members accept and push it (it succeeds)**

Add the following line in your file: `Line added by your-teamname`

**Step 9: Team leader modify the files pushed**

**Step 10: Team members fetch and pull them**

**Step 11: Team leader modify the same line**

adding in the same line `modified by teamleader-name`

**Step 12: Team members modify the same line**

Always in the same line: `Line added by your-teamname a second time`

**Step 13: Team members try to push it but need to pull first**

You will need to pull the changes first as it has been modified by the team leader. You want to stay in sync. 

**Step 14: Team members solve merge conflict**

![img/merge-conflict.png](http://i.imgur.com/2cDov13.png)

Open the file in an editor and keep what you consider relevant (at this point this is often a good idea to contact the team member having modified the same line to coordinate).

**Step 15: Team members push**

Et voilà!

## Exercise
1. Create a new repo., choose a team to add as collaborator and go through the whole process.
2. Try to create a topic branch and merge it to master at some point.
