# MarketPlace v2 Backend


# Installation

- You need to install docker-compose.
- Copy the file `env.example` to `.env`
- Execute `docker-compose -f dev.yml build`
- Execute `docker-compose -f dev.yml run --rm cumrocket_django python manage.py migrate`
- That's all!

This will create a simple development environment with a db.sqlite3 database. If you want to create a superuser you must execute the following command:

`docker-compose run --rm cumrocket_django python manage.py createsuperuser` and follow the console instructions (name, email, password...).


# Development

- All the changes must be pushed against the `development` branch using PRs. No direct commits to `development` are allowed.


# API definition

- In order to avoid to deploy a Swagger, which takes some time to configure all the custom endpoints, we are 
  delivering the Insomnia docs, which contains already all the methods, endpoint, and several examples on how to 
  interact with the API.
  The file is called `api_definition.json` and you can use it with the program [Insomnia](https://insomnia.rest/)


# KYCs

- Moved from kyc.cumrocket.io to api.cumrocket.io and being integrated in the general backend.
- This apps lets perform the KYC to the models, by submiting their name, ID pictures, birthdate, etc.


# Wallets

- This app will handle the different backend wallets that will be used to sell cummies using FIAT. 


# Catalog

- This app saves all the collections for each models and the NFTs that are part of each collection. 
  The NFTs are minted to the IPFS, but a copy is stored in the S3 in order to deliver faster the NFTs to users.
  

# Ads

- With this app we can deliver to the frontend different ads based on the spot they are going to be shown. 
  Different sizes are supported, as well as an algorithm to rotate the ads based on clicks and renders.