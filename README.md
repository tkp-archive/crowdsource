# crowdsource
Crowdsourcing answers

[![Build Status](https://travis-ci.org/timkpaine/crowdsource.svg?branch=master)](https://travis-ci.org/timkpaine/crowdsource)
[![GitHub issues](https://img.shields.io/github/issues/timkpaine/crowdsource.svg)]()
[![codecov](https://codecov.io/gh/timkpaine/crowdsource/branch/master/graph/badge.svg?token=fQFntZ90kS)](https://codecov.io/gh/timkpaine/crowdsource)
[![PyPI](https://img.shields.io/pypi/l/crowdsource.svg)](https://pypi.python.org/pypi/crowdsource)
[![PyPI](https://img.shields.io/pypi/v/crowdsource.svg)](https://pypi.python.org/pypi/crowdsource)
[![Docs](https://readthedocs.org/projects/crowdsource/badge/?version=latest)](http://crowdsource.readthedocs.io/en/latest/?badge=latest)
[![Gitter](https://img.shields.io/gitter/room/nwjs/nw.js.svg)](https://gitter.im/crowd_source/Lobby)

## Installation
`python setup.py install`

## Quick Example
In three separate terminals, run the following in order (from the examples folder)

`python -m crowdsource.server`

`python client1.py`

`python client2.py`

- Both client1 and client2 will register with the server
- Client 1 will subscribe two dummy competition functions, which will execute on any competition of type 'classify'
- Client2 will submit a dummy competition
- Client1 will automatically fetch and execute their routines on this, and their result will be submitted
- Client2 will pause, then fetch the leaderboards
- Client2 will submit a new dummy competition
- Client1 will automatically fetch and execute their routines on this, and their result will be submitted
- Client2 will pause, then fetch the leaderboards

Here is the example output:

#### Server
```text
2017-10-02 15:16:25,588 INFO -- MainProcess server.py:207 -- Server listening on port: 8889
2017-10-02 15:16:26,636 INFO -- MainProcess server.py:68 -- New request from ANON
2017-10-02 15:16:26,636 INFO -- MainProcess server.py:41 -- Registering new client 8323
2017-10-02 15:16:26,636 INFO -- MainProcess web.py:2063 -- 200 POST /register (127.0.0.1) 0.99ms
2017-10-02 15:16:26,641 INFO -- MainProcess web.py:2063 -- 200 GET /competition (127.0.0.1) 0.53ms
2017-10-02 15:16:27,674 INFO -- MainProcess server.py:68 -- New request from 1234
2017-10-02 15:16:27,674 INFO -- MainProcess server.py:41 -- Registering known client 1234
2017-10-02 15:16:27,675 INFO -- MainProcess web.py:2063 -- 200 POST /register (127.0.0.1) 0.77ms
2017-10-02 15:16:27,681 INFO -- MainProcess server.py:119 -- New request from 1234
2017-10-02 15:16:27,685 INFO -- MainProcess server.py:41 -- Registering competition 3675 from 1234
2017-10-02 15:16:27,685 INFO -- MainProcess web.py:2063 -- 200 POST /competition (127.0.0.1) 4.90ms
2017-10-02 15:16:28,649 INFO -- MainProcess web.py:2063 -- 200 GET /competition (127.0.0.1) 0.71ms
2017-10-02 15:16:28,663 INFO -- MainProcess server.py:175 -- New submission from 8323
2017-10-02 15:16:28,665 INFO -- MainProcess web.py:2063 -- 200 POST /submission (127.0.0.1) 2.54ms
2017-10-02 15:16:28,668 INFO -- MainProcess server.py:175 -- New submission from 8323
2017-10-02 15:16:28,670 INFO -- MainProcess web.py:2063 -- 200 POST /submission (127.0.0.1) 1.99ms
2017-10-02 15:16:30,682 INFO -- MainProcess web.py:2063 -- 200 GET /competition (127.0.0.1) 0.66ms
2017-10-02 15:16:31,694 INFO -- MainProcess web.py:2063 -- 200 GET /submission (127.0.0.1) 0.47ms
2017-10-02 15:16:31,701 INFO -- MainProcess server.py:119 -- New request from 1234
2017-10-02 15:16:31,705 INFO -- MainProcess server.py:41 -- Registering competition 6716 from 1234
2017-10-02 15:16:31,705 INFO -- MainProcess web.py:2063 -- 200 POST /competition (127.0.0.1) 5.01ms
2017-10-02 15:16:32,691 INFO -- MainProcess web.py:2063 -- 200 GET /competition (127.0.0.1) 1.00ms
2017-10-02 15:16:32,704 INFO -- MainProcess server.py:175 -- New submission from 8323
2017-10-02 15:16:32,706 INFO -- MainProcess web.py:2063 -- 200 POST /submission (127.0.0.1) 2.42ms
2017-10-02 15:16:32,710 INFO -- MainProcess server.py:175 -- New submission from 8323
2017-10-02 15:16:32,711 INFO -- MainProcess web.py:2063 -- 200 POST /submission (127.0.0.1) 1.87ms
2017-10-02 15:14:55,765 INFO -- MainProcess web.py:2063 -- 200 GET /competition (127.0.0.1) 0.85ms
```

#### Client 1
```text
2017-10-02 15:10:28,969 DEBUG -- MainProcess connectionpool.py:396 -- http://0.0.0.0:8889 "POST /register HTTP/1.1" 200 4
2017-10-02 15:10:28,974 DEBUG -- MainProcess connectionpool.py:396 -- http://0.0.0.0:8889 "GET /competition HTTP/1.1" 200 2
2017-10-02 15:10:28,975 DEBUG -- MainProcess connectionpool.py:396 -- http://0.0.0.0:8889 "GET /competition HTTP/1.1" 200 2
2017-10-02 15:10:30,983 DEBUG -- MainProcess connectionpool.py:396 -- http://0.0.0.0:8889 "GET /competition HTTP/1.1" 200 40969
2017-10-02 15:10:30,986 DEBUG -- MainProcess connectionpool.py:396 -- http://0.0.0.0:8889 "GET /competition HTTP/1.1" 200 40969
Answering
Answering
2017-10-02 15:10:31,013 DEBUG -- MainProcess connectionpool.py:396 -- http://0.0.0.0:8889 "POST /submission HTTP/1.1" 200 0
2017-10-02 15:10:31,017 DEBUG -- MainProcess connectionpool.py:396 -- http://0.0.0.0:8889 "POST /submission HTTP/1.1" 200 0
2017-10-02 15:10:31,023 DEBUG -- MainProcess connectionpool.py:396 -- http://0.0.0.0:8889 "POST /submission HTTP/1.1" 200 0
2017-10-02 15:10:31,026 DEBUG -- MainProcess connectionpool.py:396 -- http://0.0.0.0:8889 "POST /submission HTTP/1.1" 200 0
2017-10-02 15:10:33,036 DEBUG -- MainProcess connectionpool.py:396 -- http://0.0.0.0:8889 "GET /competition HTTP/1.1" 200 40969
2017-10-02 15:10:33,037 DEBUG -- MainProcess connectionpool.py:396 -- http://0.0.0.0:8889 "GET /competition HTTP/1.1" 200 40969
2017-10-02 15:10:35,044 DEBUG -- MainProcess connectionpool.py:396 -- http://0.0.0.0:8889 "GET /competition HTTP/1.1" 200 81993
2017-10-02 15:10:35,049 DEBUG -- MainProcess connectionpool.py:396 -- http://0.0.0.0:8889 "GET /competition HTTP/1.1" 200 81993
Answering
Answering
```

#### Client 2
```text
2017-10-02 15:09:28,754 DEBUG -- MainProcess connectionpool.py:396 -- http://0.0.0.0:8889 "POST /register HTTP/1.1" 200 4
2017-10-02 15:09:28,765 DEBUG -- MainProcess connectionpool.py:396 -- http://0.0.0.0:8889 "POST /competition HTTP/1.1" 200 4
2017-10-02 15:09:32,772 DEBUG -- MainProcess connectionpool.py:396 -- http://0.0.0.0:8889 "GET /submission HTTP/1.1" 200 57
[{"competition_id":3675,"id":9180,"score":16.5787565971}]
2017-10-02 15:09:32,783 DEBUG -- MainProcess connectionpool.py:396 -- http://0.0.0.0:8889 "POST /competition HTTP/1.1" 200 3
2017-10-02 15:09:36,794 DEBUG -- MainProcess connectionpool.py:396 -- http://0.0.0.0:8889 "GET /submission HTTP/1.1" 200 112
[{"competition_id":3675,"id":9180,"score":16.5787565971},{"competition_id":6716,"id":9180,"score":16.9241123771}]
```

## Running the Server
`python -m crowdsource.server`

## Leaderboard
Navigate to `localhost:8889/leaderboard.html` to see live competition updates.
![](https://raw.githubusercontent.com/timkpaine/crowdsource/master/docs/img/leaderboard.png)

## Client API
```python
import crowdsource.client as CC
client = CC.Client('0.0.0.0:8889')  # Args are : server host
                                    #          : id
                                    #          : passphrase

client.register()      # Register with host
client.users()         # Get active users
client.competitions()  # Get active competitions
client.leaderboards()  # Get leaderboards for all competitions
c.compete('classify', foo) # Participate in classify competitions using function "foo"
```


