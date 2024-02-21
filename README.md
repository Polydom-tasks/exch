# Exch


### Run project
```docker-compose up -d --build```

All migrations will be applied

There will be three rates already present in database:
* GBP
* USD
* JPY

### API
Base course is EUR, all convertions will go through EUR.

go to http://localhost:8888/docs after successful build. \

* You will be able to call GET rates method to fetch initial data in db
* You can also update rates or create new ones in POST request 
simply by editing default currency codes. Ex: "RUB,KGS,USD,KZT"
* You can then convert any amount from source currency code to target using POST /convert method
