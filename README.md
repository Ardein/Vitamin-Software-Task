# Vitamin Software Task 

Goal of the task is to implement a new API endpoint that returns the average value across all the end-of-the-week stock price values within each calendar year for a given company.

`GET http://ardein.pythonanywhere.com//stockprices/{TICKER}`
```json
[
    {
        "year": 2015,
        "value": 198.26
    },
    {
        "year": 2016,
        "value": 201.82
    },
    {
        "year": 2017,
        "value": 200.09
    }
]

```
