=======
Client
=======

Python Client
==============
``Crowdsource``'s server API has been wrapped with a conventient to use Client API in python. 

.. code:: python
    class Client(object):
        def __init__(self, serverHost, id=None, passphrase=None):
            '''Constructor for client object

            Client is the primary API interface for
            communicating with the server

            Arguments:
                serverhost {str} -- IP/port of the competition server
                id {str} -- participant id (if known and registering on private server)
                passphrase {str} -- participant password (if applicable)
            '''
        def register(self, id=None):
            '''Register client with the competitions host'''

        def start_competition(self, competition):
            '''Host a competition

            Arguments:
                competition {CompetitionStruct} -- A competition struct
            '''

        def compete(self, competitionType, callback, **callbackArgs):
            '''Ping server for competitionId, on update call callback'''

        def leaderboards(self, submissionId=None, clientId=None, competitionId=None, type=None):
            '''Query Crowdsource server for leaderboard info
            Keyword Arguments:
              submissionId {[int/str]} -- list of submission ids to filter on
              clientId {[int/str]} -- list of client ids to filter on
              competitionId {[int/str]} -- list of competition ids to filter on
              type {[int/str]} -- list of competition types to filter on

            Returns:
              list of submissions satisfying the above filtering
            '''

        def competitions(self, clientId=None, competitionId=None, type=None):
            '''Query Crowdsource server for competition info
            Keyword Arguments:
              clientId {[int/str]} -- list of client ids to filter on
              competitionId {[int/str]} -- list of competition ids to filter on
              type {[int/str]} -- list of competition types to filter on

            Returns:
              list of competitions satisfying the above filtering
            '''

        def submit(self, competitionId, submission, submission_format=DatasetFormat.JSON):
            '''Submit answers to a competition'''

        def users(self):
            '''Return a list of active user ids'''


