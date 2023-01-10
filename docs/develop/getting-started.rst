Getting started
===============
This page will document the different steps you can take to start your template.
It will step through an *opinionated* workflow which you can choose to adopt or tweak to your needs.

After you created your new project using ``cookiecutter`` you are presented with a bunch of 
files and folders. Since the project includes a `README.md` file you probably went through its
contents and used ``poetry install`` to **setup the initial Python environment**. 

After that initial setup, you followed the guide further and **generated this documentation**
so you could host locally and read it in your favorite browser. You are now ready to start 
developing code. Step by step we will explain on a development workflow. This workflow is
based on personal experience and preference and can be changed. If you are new to coding we 
suggest to follow it more strict as it will help colleagues to assist you, perform code reviews
and get yourself accustomed to best practices. If you are an expert coder you should already now 
the importance of testing and documenting code and have a good understanding of the importance of
git.

Initialize git
--------------
Every development project should be under **revision control**.
Therefore the first thing we need to do is to initialize our git repository, create a remote (we will use
gitlab) and set everything up.

Go to https://git/ and create a new repository. You can organize it optionally under 
a (sub)group. Make sure the project is private and follow the default settings. You don't need to 
add any template files to the project, i.e. leave it empty.

When finished, you'll get an overview page with information on how to **push an existing folder**. 
We need to follow that directive since our cookiecutter created all this skeleton 
code already.

.. code-block:: bash

    $ git init
    $ git remote add origin git@gitlab.com:<repository>.git
    $ git checkout -b initial
    $ git add .
    $ git commit -m "Initial commit"
    $ git push -u origin initial

This will move all template structure under version control, create a branch *initial* and and push it 
to the remote repository as one commit with the name *Initial commit*. By default master is protected so to
integrate it with master you should initiate a merge request. See the official gitlab docs 
(https://docs.gitlab.com/ee/user/project/merge_requests/) for more information.

At this moment we have our initial project structure merged into the master branch on the remote repository.
Using just an (unprotected) master branch might be feasible when very frequent commits are combined with a strict CI/CD. 
In real life, however, it's a lot easier to just **NEVER** push directly to master. 

You should break apart your work in small pieces that can be done in a very short time, create a (feature) branch for it,
commit regularly to that branch and do a merge request to integrate your functionality into master. It's not uncommon
a branch lives for less then a day and receives commits every 15-30 minutes. The goal is to keep master as up to date
as possible and prevent difficult merges down the line which might occur if you branches live to long.

.. WARNING::
   All work should be done in a **short-lived branch** and merged into master via a **merge request**. 
