# Notes and Things

## Frameworks and Libraries
* Python 3.6+
* Django 2.0 (2.0.7 used for development)
* Latest Django Rest Framework (DRF) (3.8.2 used for development)

## Getting started
1. Clone this repo into a folder and create a virtualenv to start clean
1. Run `pip install -r requirements.txt`
1. Run `./manage.py migrate` (this step creates the database and initializes the database tables)
1. Run `./manage.py init_data`
    * This step initializes the data configuration for the spaces, DPU, and assignments. It also loads the data from the CSV into the database.
    * Take note of the Space ids that this step prints out, you will need them to query the Spaces by id.
1. Run `./manage.py runserver`
1. From another terminal window, perform API queries by connecting to `localhost:8000`, e.g.: `curl localhost:8000/space/1/count`

## API Documentation
`GET /space/<space_id>/count`

Additional optional args:
* `ts`: timestamp to get the count for, in ISO-8601 format, e.g. `2018-05-01T08:46:00Z`

Returns:

Successful lookup returns space id, timestamp used in lookup, and count at that point in time.
```
200 OK
{
  "space_id": 24,
  "ts": "2018-05-01T08:46:00Z",
  "count": 42
}
```

Querying for a space that does not exist:
```
404 Not Found
{
  "detail": "Not found."
}
```


## TimeStampedModel
All models inherit from the Django Extensions `TimeStampedModel`. This adds a `created` and `modified` field automatically, as described [here](https://django-extensions.readthedocs.io/en/latest/model_extensions.html).

## Row IDs
All models use Django's default for row id, a simple auto-incremented id field, which are deterministic and easily guessable. Production systems may want to use a UUID field or something like a [Feistel cipher](https://wiki.postgresql.org/wiki/Pseudo_encrypt) to generate zero-collision pseudo-random ids.


## Considerations & Limitations

#### Counting since "forever"
Computing a running count from all DPU sensor activity records can be (very) expensive, depending on the database and volume of records to count.

One way to address the issue is to compute a running tally for a space periodically, then apply the DPU activity since that point. There might need to be a process that periodically "zeros" a room count, if the sensor's running count starts to drift, due to late reports or missing data from DPU relocation/offlining.


#### Should the API return negative counts?
I don't have the insight into how the Space's are initialized to some value before the sensor starts counting. If the initial room count is not known, then it makes more sense that the API would report negative numbers (reporting the delta since it started tracking). If it would be nonsense that the API returns "there's -1 people currently in the space", then clamping to zero makes more sense.


#### Performance/Scaling considerations
Computing the running total with a simple SUM will likely become a huge performance bottleneck, even with indexing.

The implementation specifics would vary depending on the business's tolerance for ignoring old data over a certain age or less granularity in the accuracy of older counts.

An easy win for returning a space's current count would be to keep a running total in a key/value store, like Redis or Memcache. As the DPU records are processed, increment or decrement the DPU's 'count' value in the cache. Allow the control function to use the cached value if no timestamp is specified, and fall back to computing the SUM at a point in time, as needed, when a timestamp is supplied.

If the business requires that the count be accurate and fast, at all ages, you could still achieve acceptable performance at the cost of a potentially very large table that keeps a running count for a space, recording the new count any time it changes. Instead of SUMing across time, you'd lookup the most recent record prior to the query time and return that count. Indexing on the space and timestamp together would allow fast lookups at any point in time.

## Production Load (100k+ DPUs)
Some kind of stream processing mechanism, possibly using Kafka/LogStash/SQS or some other kind of brokering/message bus mechanism. A scalable number of instances receiving the messages from the devices, dropping them into Kafka or on to a message bus. Downstream internal services pick up the DPU reports and apply them to a 'count processor' that is keeping current counts cached and historical counts up to date. Relational/OLTP database to keep operational/transactional data, anything cachable (e.g. current counts) in a in-memory key/value store (redis, memcache). Rely on database locking and referential integrity to avoid race conditions.

Instrumenting the count lookups and the frequency for how far back user's normally query will help tune which parts of the infrastructure need the most improvement. Using an APM SaaS, like New Relic or DataDog can help quickly pinpoint performance issues.
