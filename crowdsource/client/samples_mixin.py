from .samples import (
    classify1,
    predict1,
    predict2,
    predictCorporateBonds,
    predictCitibike,
)
from .samples import (
    answerClassify1,
    answerClassify2,
    answerClassify3,
    answerPredict1,
    answerPredictCorporateBonds,
    answerPredictCitibike,
)


class SamplesMixin:
    def _sampleClassify1(self):
        self.register()
        resp = classify1(self._host, self._cookies, self._proxies)
        self._my_competitions.append(resp)

    def _sampleAnswerClassify1(self):
        self.compete("classify", answerClassify1)

    def _sampleAnswerClassify2(self):
        self.compete("classify", answerClassify2)

    def _sampleAnswerClassify3(self):
        self.compete("classify", answerClassify3)

    def _samplePredict1(self):
        self.register()
        resp = predict1(self._host, self._cookies, self._proxies)
        self._my_competitions.append(resp)

    def _sampleAnswerPredict1(self):
        self.compete("predict", answerPredict1)

    def _samplePredict2(self):
        self.register()
        resp = predict2(self._host, self._cookies, self._proxies)
        self._my_competitions.append(resp)

    def _samplePredictCorporateBonds(self):
        self.register()
        resp = predictCorporateBonds(self._host, self._cookies, self._proxies)
        self._my_competitions.append(resp)

    def _sampleAnswerPredictCorporateBonds(self):
        self.compete("predict", answerPredictCorporateBonds)

    def _samplePredictCitibike(self):
        self.register()
        resp = predictCitibike(self._host, self._cookies, self._proxies)
        self._my_competitions.append(resp)

    def _sampleAnswerPredictCitibike(self):
        self.compete("predict", answerPredictCitibike)
