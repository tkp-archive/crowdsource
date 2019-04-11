import time
import pandas as pd
from datetime import datetime
import crowdsource.client as ac
from crowdsource.utils import log

c = ac.Client('http://crowdsourcedev.azurewebsites.net')

c._sampleClassify1()

time.sleep(1)
log.debug(c.leaderboards())

c._sampleClassify1()
time.sleep(1)
log.debug(c.leaderboards())


c._samplePredict1()
time.sleep(1)
log.debug(c.leaderboards())

c._samplePredict2()
time.sleep(1)
log.debug(c.leaderboards())

time.sleep(4)
c._samplePredictCorporateBonds()
df = pd.read_json('https://bonds.paine.nyc')
tim = df[df['Name'] == 'ABC Corp'].Time.iloc[-1]
cur = datetime.strptime(tim, '%H:%M:%S')
log.debug('Submitting new competition')

time.sleep(4)
c._samplePredictCitibike()

while True:
    time.sleep(15)
    log.debug(c.leaderboards())

    # df = pd.read_json('https://bonds.paine.nyc')

    # tim = df[df['Name'] == 'ABC Corp'].Time.iloc[-1]
    # tmp_cur = datetime.strptime(tim, '%H:%M:%S')

    # if tmp_cur > cur:
    #     cur = tmp_cur
    #     log.debug('Submitting new competition')
    #     c._samplePredictCorporateBonds()
    #     # c._samplePredictCitibike()
    # else:
    #     print('not resubmitting')
