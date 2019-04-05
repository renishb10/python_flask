from datetime import datetime, timedelta

class Helper:
    def map_ssn_report(self, session):
        if session is not None:
            sessionReportModel = {
                "SessionId": str(session['_id']),
                "Status": session['status'],
                "StatusDetail": session['statusDetail'],
                "StartOn": self.mongo_dt_to_utc_format(session['startDate']),
                "EndOn": self.mongo_dt_to_utc_format(session['endDate']),
                "Duration": None,
                "SessionType": None,
                "ConnectionType": None,
                "Title": session['title'],
                "Note": session['notes']['value'] if session['notes'] != None else None,
                "RecoupedSessionId": session['statusDetail']['recoupreeSessionId'] if session['statusDetail'] != None else None,
                "LearnerId": session['learnerId'],
                "IsPayable": session['isPayable'],
                "LicenseID": None,
                "LicenseStartDate": None,
                "LicenseEndDate": None,
                "LearnerFullName": None,
                "TrainerId": session['hostId'],
                "TrainerFullName": None,
                "RatingScore": session['feedback']['points'] if session['feedback'] != None else None,
                "RatingComment": session['feedback']['notes'] if session['feedback'] != None else None,
                "CreatedDate": self.mongo_dt_to_utc_format(session['createdDate']),
                "LastUpdatedDate": self.mongo_dt_to_utc_format(session['createdDate']),
                "StatusHistory": session['statusHistory']
            }
        return sessionReportModel

    def mongo_dt_to_utc_format(self, dt):
        return datetime.strftime(dt, "%Y-%m-%dT%H:%M:%S.%fZ") if dt != None else None

    def mongo_query_builder(self, _filterDt=None, _startDt=None, _endDt=None, _status=None, _learnerId=None, _hostId=None):
        try:
            #Form mongo query
            #By default - fetch sessions on requested day
            requestedDay = datetime.utcnow()
            requestedOneDayB4 = requestedDay - timedelta(days = 1)
            query = {
                'find' :  { 'startDate': { '$gte': requestedOneDayB4, '$lt': requestedDay }},
                'sort' : { 'startDate': 1 }
            }

            _filterDt2 = ''
            _sortOrder = 1
            if _filterDt.lower() == 'startdate':
                _filterDt2 = 'startDate'
                _sortOrder = 1
            elif _filterDt.lower() == 'lastupdateddate':
                _filterDt2 = 'lastUpdatedDate'
                _sortOrder = -1

            query['sort'] = { _filterDt2 : _sortOrder }

            if (_filterDt !=None and _startDt != None and _endDt != None and _status != None and _learnerId != None and _hostId != None):
                query['find'] = {
                    _filterDt2 : { '$gte' : _startDt, '$lt': _endDt },
                    'learnerId': _learnerId,
                    'hostId': _hostId,
                    'status': _status
                }
            elif (_filterDt != None and _startDt != None and _endDt != None and _learnerId != None and _hostId != None):
                query['find'] = {
                    _filterDt2 : { '$gte' : _startDt, '$lt': _endDt },
                    'learnerId': _learnerId,
                    'hostId': _hostId
                }

            elif (_filterDt != None and _startDt != None and _endDt != None and _status != None and _learnerId != None):
                query['find'] = {
                    _filterDt2 : { '$gte' : _startDt, '$lt': _endDt },
                    'learnerId': _learnerId,
                    'status': _status
                }
            elif (_filterDt != None and _startDt != None and _endDt != None and _learnerId != None):
                query['find'] = {
                    _filterDt2 : { '$gte' : _startDt, '$lt': _endDt },
                    'learnerId': _learnerId
                }
            elif (_filterDt != None and _startDt != None and _endDt != None and _status != None):
                query['find'] = {
                    _filterDt2 : { '$gte' : _startDt, '$lt': _endDt },
                    'status': _status
                }
            elif (_filterDt != None and _startDt != None and _endDt != None):
                query['find'] = {
                    _filterDt2 : { '$gte' : _startDt, '$lt': _endDt }
                }
            elif (_status != None):
                query['find'] = {
                    'status': _status
                }
            elif (_learnerId != None):
                query['find'] = {
                    'learnerId': _learnerId
                }
            elif (_hostId != None):
                query['find'] = {
                    'hostId': _hostId
                }

            return query
        except Exception as err:
            print(err)