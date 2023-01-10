Why a template?
===============

When we think about business intelligence, we often think just about the resulting reports, insights, or visualizations. 
While these end products are generally the main event, it's easy to focus on making the products look nice and 
ignore the quality of the code that generates them. Because these end products are created programmatically, 
code quality is still important.

It's no secret that good models are often the result of very scattershot and serendipitous explorations. 
Tentative experiments and rapidly testing approaches that might not work out are all part of the process for 
getting to the good stuff, and there is no magic bullet to turn data exploration into a simple, linear progression.

That being said, once started it is not a process that lends itself to thinking carefully about the structure 
of your code or project layout. Every data engineer tends to eventually develop their personal preferences, 
mostly learned from experience and mistakes. One has to think about what is a typical “data engineering project”, 
how it should be structured, what tools to use, and what should be taken into account. 
My vision on this is this template so everyone can start with a clean, logical structure and stick to it throughout. 
We think it's a pretty big win all around to use a fairly standardized setup like this one.

Project Organization
====================
Overview of the organization within this project. It's a high level breakdown of the different folders with
a short indication of what's the concept behind them.

::

    
    ├── docs               <- A default Sphinx project
    ├── notebooks          <- a place to put your jupyter notebooks!
    ├── tasks              <- taks for invoke commands, see `inv -l`.
    ├── tests              <- Tests collection for pytest
    │
    ├── project
    │   │
    │   └── __init__.py    <- Makes this folder a Python package
    │
    ├── .bumpversion.cfg   <- bumpversion config file
    ├── .flake8            <- flake8 config file
    ├── .gitchangelog.rc   <- gitchangelog config file
    ├── .gitignore         <- to configure which files should not go to git
    ├── .gitlab-ci.yml     <- ci/cd pipeline for gitlab
    ├── .pylintrc          <- pylint ocnfig file
    ├── README.md          <- The top-level README for developers using this project.
    ├── pyproject.toml     <- The poetry config file for reproducing the environment, e.g.
    │                         generated with `poetry install` and activated with `poetry shell`


Disagree with a couple of the default folder names? Working on a project that's a little nonstandard and doesn't exactly 
fit with the current structure? Prefer to use a different package than one of the defaults?

**Go for it!** This is a lightweight structure, and is intended to be a good starting point for many projects.

    Consistency within a project is more important. Consistency within one module or function is the most important. 
    **However**, know when to be inconsistent! Sometimes style guide recommendations just aren't applicable. 
    When in doubt, use your best judgment. Look at other examples and decide what looks best. And don't hesitate to ask!

    -- PEP8

Opinions
========
There are some opinions implicit in the project structure that have grown out of our experience with what works and 
what doesn't when collaborating on data science projects. Some of the opinions are about workflows, and some of the 
opinions are about tools that make life easier. 

Notebooks are for exploration and communication
-----------------------------------------------
This project includes jupyter notebook support which is very effective for exploratory data analysis. 
However, it can be less effective for reproducing an analysis. When we use notebooks in our work, we often subdivide the notebooks folder. 
For example, notebooks/exploratory contains initial explorations, whereas notebooks/reports is more polished work 
that can be exported as html to the reports directory.
Since notebooks are challenging objects for source control (e.g., diffs of the json are often not human-readable and merging is near impossible), 
we recommended not collaborating directly with others on Jupyter notebooks. 
There are two steps we recommend for using notebooks effectively:

1. Follow a naming convention that shows the owner and the order the analysis was done in. 
We use the format ``<step>-<ghuser>-<description>.ipynb`` (e.g., 0.3-bull-visualize-distributions.ipynb).

2. Refactor the good parts. Don't write code to do the same task in multiple notebooks. 
If it's useful utility code, refactor it and organise it to the source folder.

See the notebook documentation on how to use this refactored code on the fly within your notebook.

Build from the environment up
-----------------------------
The first step in reproducing an analysis is always reproducing the computational environment it was run in. 
You need the same tools, the same libraries, and the same versions to make everything play nicely together.

This project template uses ``poetry`` to setup and manage the python dependencies.

Keep secrets and configuration out of version control
-----------------------------------------------------
You really don't want to leak your Openshift secret key or Hana username and password on git. 
Enough said — see the Twelve Factor App principles on this point. Here's one way to do this:

Store your secrets and config variables in a special file
Create a .env file in the project root folder. Thanks to the .gitignore, this file should never get committed into the version control repository. Here's an example:

:: 

    # example .env file
    DATABASE_URL=postgres://username:password@localhost:5432/dbname
    AWS_ACCESS_KEY=myaccesskey
    AWS_SECRET_ACCESS_KEY=mysecretkey
    OTHER_VARIABLE=something

Use a package to load these variables automatically like `python-dotenv`.

Be conservative in changing the default folder structure
--------------------------------------------------------
To keep this structure broadly applicable for many different kinds of projects, we think the best approach is to be liberal 
in changing the folders around for your project, but be conservative in changing the default structure for all projects.

Result is a package
---------------------
The scope of this project template is limited to deliver a **versioned python package** or a simple **data pipeline**. In our opinion it's best
to focus on one thing only and do it well. Applying a modular approach in the devops cycle enables much more flexibility down the road.
This template makes it easy to encapsulate your developed source code into a package which can be published on a central repository,
like pypy or a private artifactory if you have access to one. Even if you only build locally or as an artifact attached to
the git repository you can easily integrate it somewhere else. For instance, other projects where you want to reuse your
functionality, notebook environments, but it also makes it straightforward to expose your functionality in a dedicated API template or
containerized application. 
The suggested workflow here is: python package -> container building -> deployment. Splitting these steps apart into modular entities,
each based on best practices templates in function of application, creates a transparant system of building blocks to organize your
specific needs within your project.
