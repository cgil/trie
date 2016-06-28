# Tote
Tote - mcommerce reimagined.
A service for drag-and-drop in-app mobile stores.
You host one of our stores and we handle customer service, inventory management, logistics, and tracking.

A new way to monetize your app without depending on ads.

![Tote Store landing page](https://raw.githubusercontent.com/cgil/trie/master/trie/static/images/home_landing_page.png "Home screen image.")

# Trie
The backend for Tote handling logistics, payments, and customer data.

# Bootstrap
```
# Set up your environment
$ cd trie
$ virtualenv env
$ source env/bin/activate

$ pip install fabric
# Bootstrap dependencies
$ fab bootstrap
# Bootstrap the database
$ fab bootstrap_database
```

# Testing
```
# After bootstrapping
$ fab test
```

# Running locally
```
# Run a local server
fab serve
```

# Running in production
This project is set up to quickly bootstrap into Heroku, although running running on any host is easily achievable.
Update the heroku configuration to quickly launch on a Heroku instance.

# Fabric
This repo uses Fabric, check out the `fabfile.py` for all runnable commands.
We also use `manage.py` as a hook for heroku commands, especially migrations.

# Migrations on production (Heroku)
```
# Migrate to head.
heroku db upgrade head

# Upgrade +X revisions.
heroku db upgrade +1

# Downgrade -X revisions.
heroku db downgrade -1
```

# Configuration
Update test.yaml, development.yaml, production.yaml accordingly with appropriate credentials.
We use sendgrid, stripe, and any email provider of your choice.

# Scripts
There exist a few scripts to collect emails from apps that have already shown interest in you and send out bulk messages created to facilitate outreach.
These are here for educational purposes and should only be used as reference.
I do not support or am I responsible for any misuse of any information provided.
In no way should you use the information to cause any kind of damage directly or indirectly.
