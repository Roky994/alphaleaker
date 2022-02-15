# AlphaLeaker

Get alpha regarding cryptocurrencies.

# Requirements

- $ pip install -U python-dotenv

# Services

## Trends

Provides trending cryptocurrencies.
Data is provided bz [https://apewisdom.io/](apewisdom.io) API.

- Running
```
python trends.py
```

- Running migrations

```
python trends.py migrate [drop]
```

## Tweets

Provides new tweets from marked users

- Running
```
python tweets.py
```

## Sniper

Provides new twitter accounts with possible new projects

- Running
```
python sniper.py
```