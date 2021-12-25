# CurrencyApp
## Set up Process

1. ### Env File Creation
⋅⋅⋅ Create an env file (`.env`) file in the root of the project with the following content:

```
REDIS_URL=redis://redis/0
DJANGO_SECRET_KEY=123
DJANGO_DEBUG=True
```

2. ### `make build`

⋅⋅⋅ This command will install all the dependencies in [requirements.txt](requirements.txt) with `docker-compose build`.

⋅⋅⋅ After all dependencies are installed, this will run `python manage.py migrate`

---

## Run the project

### `make run`

This command will run `docker-compose up` and will run your django server in the URL: `localhost:8060`.

---

More available commands in [Makefile](Makefile)

## Work
### go to swager
open http://0.0.0.0:8000/swagger-ui/

#### First Create user
method: register

#### Autorize
Enter your user from Register
#### Post currency

Change Json for select data:exchangedate of target dete\
or use min_exchangedate and max_exchangedate for date range

```
{
    "exchangedate": "2021-12-25",
    "min_exchangedate": "2021-12-25",
    "max_exchangedate": "2021-12-25"
}
```