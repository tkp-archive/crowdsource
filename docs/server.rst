=======
Server
=======

Running a server
=================

``Crowdsource`` Provides a server out of the box, which you can run with:

.. code:: bash

    python -m crowdsource.server


Server API
===========
The server provides a json API to integrate with other languages/services. We also provide a python client which nicely wraps the API.

Login
------
``GET /api/v1/login``

Args:

Response:

.. code:: json

    {"id": 1325}


``POST /api/v1/login``

Args:

Response:


Logout
-------
``GET /api/v1/logout``

Args:

Response:


``POST /api/v1/logout``

Args:

Response:



Register
---------
``GET /api/v1/register``

Args:

Response:

.. code:: json

    [{"id":"6981"},{"id":"6788"},{"id":"2148"}]

``POST /api/v1/register``

Args:

Response:


Competitions
------------
``GET /api/v1/competitions``

Args:

Response:

.. code:: json

    [{"type":"classify","expiration":"2018-04-30 15:05:24","prize":1.0,"metric":"logloss","dataset":"{\"0\":{\"0\":-1.1627126915,\"1\":-0.5079558597,\"10\":0.0054502336,\"11\":-0.4064550346,\"12\":-0.860671341,\"13\":-0.2866074198,\"14\":-0.1187325937,\"15\":0.1329720327,\"16\":0.8014418849,\"17\":0.7742516432,\"18\":-0.4937324418,\"19\":-0.4001384878,\"2\":0.0875058003,\"20\":1.4304842543,\"21\":0.8275287298,\"22\":0.7800395268,\"23\":0.4060788076,\"24\":-0.2047205176,\"25\":-0.7925366657,\"26\":-1.0586686636,\"27\":-0.1604743319,\"28\":0.1250436049,\"29\":-1.4545456423,\"3\":-0.7443001906,\"30\":0.7475430033,\"31\":2.1755177665,\"32\":-0.013413497,\"33\":0.058122427,\"34\":0.4484005633,\"35\":-0.1688918208,\"36\":-0.1611547785,\"37\":-0.5976379193,\"38\":1.3938308688,\"39\":-1.4032058259,\"4\":-0.6961209791,\"40\":0.3007974201,\"41\":-1.5360534844,\"42\":0.1538373241,\"43\":-0.0272872758,\"44\":0.6128402512,\"45\":-0.1101918806,\"46\":-0.5905920673,\"47\":0.1321888397,\"48\":-0.1998536661,\"49\":0.2801362786,\"5\":-0.6672016993,\"50\":0.7246925325,\"51\":-0.2645704449,\"52\":-0.416957769,\"53\":-2.1410488946,\"54\":-0.6116772927,\"55\":0.7647256496,\"56\":0.7169255905,\"57\":1.0187816203,\"58\":0.2319432665,\"59\":0.6846735112,\"6\":2.0335035268,\"60\":-0.8754182379,\"61\":0.9867173008,\"62\":0.0620626707,\"63\":1.2590084254,\"64\":1.2308778098,\"65\":-0.3802143878,\"66\":0.6059718244,\"67\":0.9978396334,\"68\":0.7007951872,\"69\":0.9875920657,\"7\":-0.7464666084,\"70\":-0.5252532523,\"71\":-1.7520431711,\"72\":-0.8038865908,\"73\":1.9135007796,\"74\":-0.1125711662,\"75\":0.5142515645,\"76\":-0.8079307036,\"77\":-0.3228957449,\"78\":1.6874338071,\"79\":1.1423945339,\"8\":0.6214777904,\"80\":0.1446751391,\"81\":0.2764658512,\"82\":-0.1943676294,\"83\":0.1345252404,\"84\":1.1416954694,\"85\":-1.371343468,\"86\":0.1955380044,\"87\":-1.2328143618,\"88\":1.671244442,\"89\":-1.246932196,\"9\":1.0713792888,\"90\":1.5437755794,\"91\":0.7394898313,\"
    ...

``POST /api/v1/competitions``

Args:

Response:

Submissions
------------
``GET /api/v1/submissions``

Args:

Response:

.. code:: json

    [{"competitionId":"3198","answer":"{\"0\":{\"0\":0,\"1\":0,\"10\":0,\"11\":0,\"12\":0,\"13\":0,\"14\":0,\"15\":0,\"16\":1,\"17\":1,\"18\":0,\"19\":0,\"2\":0,\"20\":1,\"21\":1,\"22\":1,\"23\":0,\"24\":0,\"25\":0,\"26\":0,\"27\":0,\"28\":0,\"29\":0,\"3\":0,\"30\":1,\"31\":1,\"32\":0,\"33\":0,\"34\":0,\"35\":0,\"36\":0,\"37\":0,\"38\":1,\"39\":0,\"4\":0,\"40\":0,\"41\":0,\"42\":0,\"43\":0,\"44\":1,\"45\":0,\"46\":0,\"47\":0,\"48\":0,\"49\":0,\"5\":0,\"50\":1,\"51\":0,\"52\":0,\"53\":0,\"54\":0,\"55\":1,\"56\":1,\"57\":1,\"58\":0,\"59\":1,\"6\":1,\"60\":0,\"61\":1,\"62\":0,\"63\":1,\"64\":1,\"65\":0,\"66\":1,\"67\":1,\"68\":1,\"69\":1,\"7\":0,\"70\":0,\"71\":0,\"72\":0,\"73\":1,\"74\":0,\"75\":1,\"76\":0,\"77\":0,\"78\":1,\"79\":1,\"8\":1,\"80\":0,\"81\":0,\"82\":0,\"83\":0,\"84\":1,\"85\":0,\"86\":0,\"87\":0,\"88\":1,\"89\":0,\"9\":1,\"90\":1,\"91\":1,\"92\":0,\"93\":1,\"94\":0,\"95\":1,\"96\":0,\"97\":0,\"98\":0,\"99\":1}}","answer_type":"json","id":"9634","clientId":"6788","active":false,"timestamp":"2018-04-30 15:04:25","type":"classify","score":18.31,"expiration":"2018-04-30 15:05:24","metric":"logloss"},{"competitionId":"3198","answer":"{\"0\":{\"0\":0,\"1\":0,\"10\":0,\"11\":0,\"12\":0,\"13\":0,\"14\":0,\"15\":0,\"16\":1,\"17\":1,\"18\":0,\"19\":0,\"2\":0,\"20\":1,\"21\":1,\"22\":1,\"23\":1,\"24\":0,\"25\":0,\"26\":0,\"27\":0,\"28\":0,\"29\":0,\"3\":0,\"30\":1,\"31\":1,\"32\":0,\"33\":0,\"34\":1,\"35\":0,\"36\":0,\"37\":0,\"38\":1,\"39\":0,\"4\":0,\"40\":1,\"41\":0,\"42\":0,\"43\":0,\"44\":1,\"45\":0,\"46\":0,\"47\":0,\"48\":0,\"49\":1,\"5\":0,\"50\":1,\"51\":0,\"52\":0,\"53\":0,\"54\":0,\"55\":1,\"56\":1,\"57\":1,\"58\":1,\"59\":1,\"6\":1,\"60\":0,\"61\":1,\"62\":0,\"63\":1,\"64\":1,\"65\":0,\"66\":1,\"67\":1,\"68\":1,\"69\":1,\"7\":0,\"70\":0,\"71\":0,\"72\":0,\"73\":1,\"74\":0,\"75\":1,\"76\":0,\"77\":0,\"78\":1,\"79\":1,\"8\":1,\"80\":0,\"81\":1,\"82\":0,\"83\":0,\"84\":1,\"85\":0,\"86\":0,\"87\":0,\"88\":1,\"89\":0,\"9\":1,\"90\":1,\"91\":1,\"92\":1,\"93\":1,\"94\":0,\"95\":1,\"96\":0,\"97\":0,\"98\":0,\"99\":1}}","answer_type":"json","id":"6227","clientId":"6788","active":false,"timestamp":"2018-04-30 15:04:25","type":"classify","score":17.27,"expiration":"2018-04-30 15:05:24","metric":"logloss"},{"competitionId":"3198","answer":"{\"0\":{\"0\":0,\"1\":0,\"10\":0,\"11\":0,\"12\"
    ...


``POST /api/v1/submissions``

Args:

Response:


Leaderboards
-------------
``GET /api/v1/leaderboards``

Args:

Response:


``POST /api/v1/leaderboards``

Args:

Response:


Integrating with server
========================

By default, the ``Crowdsource`` server comes with no authentication. It can be configured to run against a postgres database by including the ``--sql`` flag. However, give the target is internal systems, it is recommended to provide your own integrations, as follow.


``Crowdsource`` provides an instance of ``tornado.web.Application``, which is customized with several handlers. 

.. code:: python

    class ServerApplication(tornado.web.Application):
        def __init__(self, login, register, persist, basepath="/", handlers=None, cookie_secret=None, debug=True):


Lets walk through what these functions and data structures are, and what custom instances should do.


Login
------
The custom login function takes a handler and a user token (possible null), and returns an instance of a ClientStruct or None (indicating the user is not authenticated).

.. code:: python

    def login(handler, user):
        '''
        handler: instance of crowdsource.handlers.ServerHandler
        user: user token from secret cookie
        returns: crowdsource.Structs.ClientStruct or None
        '''


Register
--------
Similarly, the custom register function takes a handler and user registration data (in a dictionary) and returns an instance of a ClientStruct.

.. code:: python

    def register(handler, data):
        '''
        handler: instance of crowdsource.handlers.ServerHandler
        data: dictionary containing registration information
        returns: crowdsource.Structs.ClientStruct
        '''

Persist
--------
The ``persist`` function is used to stash clients, competitions, and submissions. 

.. code:: python

    def persist(handler, struct, update=False, *args, **kwargs):
        '''
        handler: instance of crowdsource.handlers.ServerHandler
        struct: an instance of crowdsource.Structs.{ClientStruct, CompetitionStruct, SubmissionStruct}
        returns: None
        '''


Handlers
--------
Any of the default handlers can be overridden with custom handlers passed in the ``handlers`` argument (as a list). Handlers are replaced based on path name, so be sure to match a default handler:

.. code:: python

    [(r"/", HTMLOpenHandler)
     (r"/index.html", HTMLOpenHandler),
     (r"/login", HTMLOpenHandler),
     (r"/register", HTMLOpenHandler),
     (r"/logout", HTMLOpenHandler),
     (r"/competitions", HTMLHandler),
     (r"/submissions", HTMLHandler),
     (r"/leaderboard", HTMLHandler),
     (r"/api/v1/login", LoginHandler),
     (r"/api/v1/logout", LogoutHandler),
     (r"/api/v1/register", RegisterHandler),
     (r"/api/v1/competition", CompetitionHandler),
     (r"/api/v1/submission", SubmissionHandler),
     (r"/api/v1/leaderboard", LeaderboardHandler),
     (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": static}),
     (r"/(.*)", HTMLOpenHandler, {'template': '404.html'})]

