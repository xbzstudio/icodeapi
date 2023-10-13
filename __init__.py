'''
### icodeapi

icodeapi is a framework to help you control your icodeshequ account in python.

Documents: [https://xbz-studio.gitbook.io/icodeapi](https://xbz-studio.gitbook.io/icodeapi).

turingAPI documents: [https://xbz-studio.gitbook.io/turingapi](https://xbz-studio.gitbook.io/turingapi)

------

by [xbzstudio](https://xbz-studio.gitbook.io)
'''

import urllib3, urllib.parse, httpx, warnings
from typing import Union

DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203'

class LoginWarning(Warning):
    pass

class LoginError(Exception):
    pass

class IcodeAPI():
    '''
        Create a icodeshequ user.

        Go to https://icodeshequ.youdao.com to get your cookies.
    '''
    __cookie : str = ''
    userAgent : str = DEFAULT_USER_AGENT
    __info : dict = {}
    client : httpx.Client = None
    __loginStatus = False

    def __init__(self, cookie : str = '', userAgent : str = DEFAULT_USER_AGENT, httpxClient : httpx.Client = httpx.Client(), timeout : Union[int, float] = 10):
        self.__cookie = cookie.encode('utf-8')
        self.userAgent = userAgent
        self.client = httpxClient
        self.client.timeout = timeout
        self.login()


    def login(self, newCookie : str = None) -> dict:
        '''
        Login to https://icodeshequ.youdao.com use self.__cookie.

        This function will return a dict, and the dict always be like:
        ```python
            {
                'encryptionUserId': str,
                'userId': str, 
                'name': str, 
                'image': str, 
                'permissions': list, 
                'mobile': str, 
                'hasCourse': bool, 
                'userIdentity': str,
                'courseType': str
            }
        ```
        '''
        if newCookie:
            self.__cookie = newCookie.encode('utf-8')
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        response = self.client.get('https://icodecontest-online-api.youdao.com/api/user/info', headers = headers)
        if not (data := response.json()).get('code'):
            result = data.get('data')
            self.__loginStatus = True
            self.__info = result
            return result
        else:
            result = {}
            warnings.warn('Login failed', LoginWarning)
            self.__loginStatus = False
            self.__info = result
            return result
        
    def getLoginStatus(self):
        return self.__loginStatus
    
    def getInfo(self):
        return self.__info
    
    def getWorkDetail(self, workId : str, addBrowseNum : bool = True) -> dict:
        '''
        Get work detail.

        This function will return a dict, and the dict always be like:
        ```python
        {
            'id': str, 
            'title': str, 
            'imgUrl': str, 
            'description': str,
            'type': int,
            'userId': str,
            'status': int,
            'likeNum': int,
            'browseNum': int,
            'enshrineNum': int,
            'code': str,
            'userName': str, 
            'userImage': str, 
            'haveLiked': bool ,
            'haveEnshrined': bool,
            'createTimeStr': str, 
            'updateTimeStr': str, 
            'codeLanguage': str, 
            'shortLink': str, 
            'theme': str, 
            'subTheme': str, 
            'iframeUrl': str, 
            'scratchFile': str, 
            'codeType': str, 
            'firstPopups': bool , 
            'forkAuthorizationStatus': bool, 
            'isFirstPublish': bool, 
            'haveReported': bool
        }
        ```
    '''
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        response = self.client.get(f'https://icodeshequ.youdao.com/api/works/detail?id={workId}&addBrowseNum={str(addBrowseNum).lower()}', headers = headers)
        result = response.json()['data']
        return result
    
    def getWorkComments(self, workId : str, page : int = 1, getNum : int = 20) -> list:
        '''
        Get work comments.
        
        This function will return a list, and the list always be like:
        ```python
        [
            {
                'id': int, 
                'content': str, 
                'userId': str, 
                'name': str, 
                'image': str, 
                'isAuthor': bool, 
                'praiseNum': int, 
                'replyNum': int, 
                'time': int, 
                'hasPraised': bool
            }
        ]
        ```
        '''
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        response = self.client.get(f'https://icodeshequ.youdao.com/api/works/comment/list?id={workId}&page={page}&size={getNum}', headers = headers)
        result = response.json().get('dataList')
        return result
    
    def getMoreWorks(self, userId : str = None, workId : str = None) -> list:
        '''
        Get more works.

        This function will return a list, and the list always be like:
        ```python
        [
            {
                'id': str, 
                'title': str, 
                'imgUrl': str, 
                'likeNum': int, 
                'browseNum': int, 
                'userName': str, 
                'userImage': str
            }
        ]
        ```
        '''
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        if userId or workId:
            if userId == None:
                userId = self.getWorkDetail(workId)['userId']
                response = self.client.get(f'https://icodeshequ.youdao.com/api/user/more_works/list?userId={userId}&currentWorksId=21a8bbf470ef4203abd549c641aac7a6')
                result = response.json().get('dataList')
            else:
                response = self.client.get(f'https://icodeshequ.youdao.com/api/user/more_works/list?userId={userId}&currentWorksId=21a8bbf470ef4203abd549c641aac7a6', headers = headers)
                result = response.json().get('dataList')
            return result
        else:
            raise ValueError('Both userId and workId are None')
        
    def getWorks(self, page : int = 1, getNum : int = 20, sortType : int = 2, theme : str = 'all', codeLanguage : str = 'all', keyword : Union[str, any] = '') -> list:
        '''
        Get works.
        
        Parameters
        ----------
        `page` : int, default 1
            Page number.
        `getNum` : int, default 20
            Number of works per page.
        `sortType` : int, default 1
            Sort type.

            1: Most likes

            2: Newest
        `theme` : str, default 'all'
            Work theme in icodeshequ.

            'all': All themes

            'play': Games theme

            'story': Story theme

            'art': Art theme

            'minecraft': Minecraft theme, the works about Minecraft

            'scratch': Scratch works

            'turtle': Python works
        `codeLanguage` : str, default 'all'
            The code language of works.

            'all': All code language

            'blockly': Blockly works

            'scratch': Scratch works

            'python': Python works
        `keyword` : str, default ''
            The key word of works.
        ----------

        This function will return a list, and the list always be like:
        ```python
            [
                {
                    'id': str, 
                    'title': str, 
                    'imgUrl': str, 
                    'userId': str, 
                    'browseNum': int, 
                    'userName': str, 
                    'userImage': str, 
                    'codeLanguage': str
                }
            ]
        ```
        '''
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        response = self.client.get(f'https://icodeshequ.youdao.com/api/index/works/list?page={page}&size={getNum}&sortType={sortType}&theme={theme}&codeLanguage={codeLanguage}&keyword={keyword}', headers = headers)
        result = response.json().get('dataList')
        return result
    
    def getMyWorks(self, page : int = 1, getNum : int = 20, theme : str = 'all', codeLanguage : str = 'all', status : int = 2, keyword : Union[str, any] = '') -> list:
        '''
        Get user works.

        Parameters
        ----------
        `page` : int, default 1
            Page number.
        `getNum` : int, default 20
            Number of works per page.
        `theme` : str, default 'all'
            Work theme in icodeshequ.

            'all': All themes

            'play': Games theme

            'story': Story theme

            'art': Art theme

            'minecraft': Minecraft theme, the works about Minecraft

            'scratch': Scratch works

            'turtle': Python works
        `codeLanguage` : str, default 'all'
            The code language of works.

            'all': All code language

            'blockly': Blockly works

            'scratch': Scratch works

            'python': Python works
        `status` : int, default 2
            The publishing status of works

            1: No published

            2: Published
        `keyword` : str, default ''
            The key word of works.
        ----------

        This function will return a list, and the list always be like:
        ```python
        [
            {
                'id': str, 
                'title': str, 
                'imgUrl': str, 
                'status': int,
                'likeNum': int, 
                'browseNum': int, 
                'enshrineNum': int, 
                'forkNum': int, 
                'userName': str, 
                'userImage': str, 
                'codeLanguage': str, 
                'theme': str, 
                'subTheme': str
            }
        ]
        ```
        '''
        if not self.__loginStatus:
            raise LoginError('User is not logged in')
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        response = self.client.get(f'https://icodeshequ.youdao.com/api/user/works/list?page={page}&size={getNum}&status={status}&theme={theme}&codeLanguage={codeLanguage}&keyword={keyword}', headers = headers)
        result = response.json().get('dataList')
        return result
    
    def getWorkSubmitInfo(self, workId : str) -> dict:
        '''
        Get work submit info.

        This function will return a dict, and the dict always be like:
        ```python
        {
            'avatar': str, 
            'category': str, 
            'codeType': str, 
            'commit': str, 
            'createtime': str, 
            'description': str, 
            'fork': int, 
            'forkcommit': str, 
            'forkfrom': str, 
            'likes': int, 
            'owner': str, 
            'publish': int, 
            'qrCodeImage': str, 
            'shareMessage': str, 
            'shareText': str, 
            'shareTitle': str, 
            'subtheme': str, 
            'theme': str, 
            'thumbnail': str, 
            'thumbnailList': list, 
            'title': str, 
            'username': str, 
            'visits': int, 
            'workid': str
        }
        ```

        When the work is a python work, the dict will be:
        ```python
        {
            'avatar': str, 
            'category': str, 
            'codeType': str, 
            'code': str,
            'commit': str, 
            'createtime': str, 
            'description': str, 
            'fork': int, 
            'forkcommit': str, 
            'forkfrom': str, 
            'likes': int, 
            'owner': str, 
            'publish': int, 
            'qrCodeImage': str, 
            'shareMessage': str, 
            'shareText': str, 
            'shareTitle': str, 
            'subtheme': str, 
            'theme': str, 
            'thumbnail': 'str, 
            'thumbnailList': list, 
            'title': str, 
            'username': str, 
            'visits': int, 
            'workid': str
        }
        ```
        '''
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        response = self.client.get(f'https://icode.youdao.com/api/work/get?id={workId}', headers = headers)
        result = response.json()
        return result
    
    def getPersonInfo(self, userId : str) -> dict:
        '''
        Get user info.

        The function will return a dict, and the dict always be like:
        ```python
        {
            'worksNum': int, 
            'viewNum': int, 
            'praiseNum': int, 
            'enshrinesNum': int, 
            'forkNum': int, 
            'userId': str, 
            'img': str, 
            'nickName': str, 
            'intro': str
        }
        ```
        '''
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        response = self.client.get(f'https://icodeshequ.youdao.com/api/user/index/hisStatics?userId={userId}', headers = headers)
        result = response.json().get('data')
        return result

    def getPersonWorks(self, userId : str, page : int = 1, getNum : int = 20) -> list:
        '''
        Get user works.

        This function will return a list, and the list always be like:
        ```
        [
            {
                'id': str, 
                'title': str, 
                'imgUrl': str, 
                'status': int, 
                'likeNum': int, 
                'browseNum': int, 
                'enshrineNum': int, 
                'forkNum': int, 
                'userName': str, 
                'userImage': str, 
                'codeLanguage': str, 
                'theme': str, 
                'subTheme': str
            }
        ]
        ```
        '''
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        response = self.client.get(f'https://icodeshequ.youdao.com/api/user/works/hisWorksList?page={page}&size={getNum}&userId={userId}', headers = headers)
        result = response.json().get('dataList')
        return result

    def getPersonEnshrines(self, userId : str, page : int = 1, getNum : int = 20) -> list:
        '''
        Get user enshrines.

        This function will return a list, and the list always be like:
        ```python
        [
            {
                'id': str, 
                'title': str, 
                'imgUrl': str, 
                'userId': str, 
                'status': int, 
                'likeNum': int, 
                'browseNum': int, 
                'userName': str, 
                'userImage': str, 
                'codeLanguage': str, 
                'theme': str, 
                'subTheme': str
            }
        ]
        ```
        '''
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        response = self.client.get(f'https://icodeshequ.youdao.com/api/user/works/hisEnshrines?page={page}&size={getNum}&userId={userId}', headers = headers)
        result = response.json().get('dataList')
        return result
    
    def getReplies(self, commentId : int, page : int = 1, getNum : int = 20) -> list:
        '''
        Get the replies of a comment.

        This function will return a list, and the list always be like:
        ```python
        [  # When this reply is a reply to a comment
            {
                "id": int,
                "content": str,
                "type": int,
                "commentId": int,
                "userId": str,
                "name": str,
                "image": str,
                "isAuthor": bool,
                "time": int,
                "praiseNum": int,
                "hasPraised": bool
            }
        ]
        [ # When this reply is a reply to an another reply
            {
                "id": int,
                "content": str,
                "type": int,
                "commentId": str,
                "userId": str,
                "name": str,
                "image": str,
                "isAuthor": bool,
                "replyUserId": str,
                "replyName": str,
                "replyImage": str,
                "time": int,
                "praiseNum": int,
                "hasPraised": bool
            }
        ]
        ```
        '''
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        response = self.client.get(f'https://icodeshequ.youdao.com/api/works/reply/list?commentId={commentId}&page={page}&size={getNum}', headers  = self.headers)
        result = response.json()['dataList']
        return result
    
    def getMessages(self, messageType : str = 'reply', page : int = 1, getNum : int = 20) -> list:
        '''
        Get the reply messages in messgaes hub.

        Parameters
        ----------
        `messageType` : str, default "reply"
            The type of messages in messages hub.

            "reply": reply message

            "enshrine": like and enshrine message

            "system": system message
        `page` : int, default 1
            Page number.
        `getNum` : int, default 20
            Number of works per page.
        ----------

        This function will return a list, and the list always be like:
        ```python
        [
            {
                'actionUserId': str,
                'actionUserImage': str,
                'actionUserName': str,
                'createTime': str,
                'createTimeStr': str,
                'haveRead': bool,
                'id': int,
                'type': int,
                'worksId': str,
                'worksTitle': str
            }
        ]
        ```
        '''
        if not self.__loginStatus:
            raise LoginError('User is not logged in')
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        match messageType:
            case 'reply':
                response = self.client.get(f'https://icodeshequ.youdao.com/api/user/message/commentMessage?page={page}&size={getNum}', headers = headers)
            case 'enshrine':
                response = self.client.get(f'https://icodeshequ.youdao.com/api/user/message/enshrinesMessage?page={page}&size={getNum}', headers = headers)
            case 'system':
                response = self.client.get(f'https://icodeshequ.youdao.com/api/user/message/systemMessage?page={page}&size={getNum}', headers = headers)
            case _:
                raise ValueError(f'messageType must be "reply" or "enshrine" or "system", not {messageType}')
        result = response.json().get('dataList')
        return result

    def getScratchAsset(self, md5ext : str):
        '''
        Get asset in scratch work.
        '''
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        response = self.client.get(f'https://ydschool-online.nosdn.127.net/svg/{md5ext}', headers = headers)
        result = response.content
        return result
    
    def comment(self, workId : str, content : str) -> dict:
        '''
        Comment a work.
        '''
        if not self.__loginStatus:
            raise LoginError('User is not logged in')
        body = {
            'id': workId,
            'content': content
        }
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        headers['Content-Type'] = 'application/json'
        response = self.client.post('https://icodeshequ.youdao.com/api/works/comment', json = body, headers = headers)
        result = response.json()
        return result
    
    def like(self, workId : str, mode : int = 1) -> dict:
        '''
        Like a work.

        If mode = 1, like the work. If mode = 2, un-like the work.
        '''
        if not self.__loginStatus:
            raise LoginError('User is not logged in')
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        url = f'https://icodeshequ.youdao.com/api/works/like?id={workId}&type={mode}'
        response = self.client.post(url, data = 'IcodeAPI: Like request'.encode('utf-8'), headers = headers)
        result = response.json()
        return result
    
    def enshrine(self, workId : str, mode : int = 1) -> dict:
        '''
        Enshrine a work.

        If mode = 1, enshrine the work. If mode = 2, un-enshrine the work.
        '''
        if not self.__loginStatus:
            raise LoginError('User is not logged in')
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        urlContent = 'enshrine' if (not (mode - 1)) else 'cancelEnshrine'
        url = f'https://icodeshequ.youdao.com/api/user/works/{urlContent}?worksId={workId}'
        response = self.client.post(url, data = 'IcodeAPI: Enshrine request'.encode('utf-8'), headers = headers)
        result = response.json()
        return result
    
    def report(self, workId : str, reason : str, reportType : int) -> dict:
        '''
        Report a work.

        reportType:
            1: plagiarize,
            2: ad spam,
            3: personal attacks,
            4: illegal,
            5: r18 / r18g
        '''
        if not self.__loginStatus:
            raise LoginError('User is not logged in')
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        body = {'worksIdStr':workId,
                'category':reportType,
                'description':reason
                }
        response = self.client.post('https://icodeshequ.youdao.com/api/works/report', json = body, headers = headers)
        result = response.json()
        return result
    
    def submitWork(self, workCode : str = '',
                   workType : str = 'Scratch', 
                   publish : int = 1,
                   save : int = False,
                   title : str = 'Scratch Project', 
                   description : str = 'Project Description', 
                   thumbnail : str = 'http://ydschool-online.nosdn.127.net/svg/0c3a986d5266bd5a186014aebd219e05c9696de777dea2b5dfe658dc661e572c.png',
                   fork : int = 0,
                   workDetail : tuple = None,
                   workId : str = None) -> dict:
        '''
        Submit a work.

        This function only supported to submit Scratch or Python work, no Blockly.

        If the workId isnt None, the function will reSubmit the work.

        When the workType is Python, and the save is true, the funciton will only save the work, not publish the work.

        If publish = 1, the function will publish the work, when it is 2, the fucntion will unpublish the work.

        If fork = 1, allow others to fork your work, if fork = 0, dont allow others to fork your work.

        If workDetail should be a tuple. workDetail[0] = `getWorkDetail()` return value, workDetail[1] = `getWorkSubmitInfo()` return value.
        '''
        if not self.__loginStatus:
            raise LoginError('User is not logged in')
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        if workDetail:
            if not workId:
                match workDetail[0].get('codeLanguage'):
                    case 'scratch':
                        fields = {
                            'category' : 'lab',
                            'code' : workDetail[0].get('code'),
                            'codeType' : 'json',
                            'theme' : 'scratch',
                            'subtheme' : 'scratch',
                            'description' : workDetail[0].get('description'),
                            'fork' : workDetail[1].get('fork'),
                            'publish' : workDetail[0].get('status') % 2 + 1,
                            'thumbnail' : workDetail[0].get('imgUrl'),
                            'title' : workDetail[0].get('title')
                        }
                        fields=urllib3.encode_multipart_formdata(fields=fields)
                        body = fields[0]
                        headers = headers
                        headers['Content-Type'] = fields[1]
                        response = self.client.post('https://icode.youdao.com/api/work/submit',data = body, headers = headers)
                    case 'python':
                        if save:
                            body = {
                                'code' : workDetail[0].get('code'),
                                'description' : workDetail[0].get('description'),
                                'title': workDetail[0].get('title')
                            }
                            headers = headers
                            headers['Content-Type'] = 'application/json'
                            response = self.client.post('https://icodeshequ.youdao.com/api/works/save', json = body, headers = headers)
                        else:
                            body = {
                                'code' : workDetail[0].get('code'),
                                'description' : workDetail[0].get('description'),
                                'title': workDetail[0].get('title'),
                                'imgUrl': workDetail[0].get('imgUrl')
                            }
                            headers = headers
                            headers['Content-Type'] = 'application/json'
                            response = self.client.post(f'https://icodeshequ.youdao.com/api/works/publish?publishType={workDetail[0].get("status") % 2 + 1}', json = body, headers = headers)
                    case _:
                        raise ValueError('Invalid workDetail.')
            else:
                match workDetail[0].get('codeLanguage'):
                    case 'scratch':
                        fields = {
                            'category' : 'lab',
                            'code' : workDetail[0].get('code'),
                            'codeType' : 'json',
                            'theme' : 'scratch',
                            'subtheme' : 'scratch',
                            'description' : workDetail[0].get('description'),
                            'fork' : workDetail[1].get('fork'),
                            'publish' : workDetail[0].get('status') % 2 + 1,
                            'thumbnail' : workDetail[0].get('imgUrl'),
                            'title' : workDetail[0].get('title'),
                            'workid' : workId
                        }
                        fields=urllib3.encode_multipart_formdata(fields=fields)
                        body = fields[0]
                        headers = headers
                        headers['Content-Type'] = fields[1]
                        response = self.client.post('https://icode.youdao.com/api/work/submit',data = body, headers = headers)
                    case 'python':
                        if save:
                            body = {
                                'code' : workDetail[0].get('code'),
                                'description' : workDetail[0].get('description'),
                                'title': workDetail[0].get('title'),
                                'id' : workId
                            }
                            headers = headers
                            headers['Content-Type'] = 'application/json'
                            response = self.client.post('https://icodeshequ.youdao.com/api/works/save', json = body, headers = headers)
                        else:
                            body = {
                                'code' : workDetail[0].get('code'),
                                'description' : workDetail[0].get('description'),
                                'title': workDetail[0].get('title'),
                                'imgUrl': workDetail[0].get('imgUrl'),
                                'id' : workId
                            }
                            headers = headers
                            headers['Content-Type'] = 'application/json'
                            response = self.client.post(f'https://icodeshequ.youdao.com/api/works/publish?publishType={workDetail[0].get("status") % 2 + 1}', json = body, headers = headers)
                    case _:
                        raise ValueError('Invalid workDetail.')
            result = response.json()
            return result
        if not workId:
            if workType in ['Scratch', 'scratch']:
                fields = [("category", (None, 'lab')), ("code", (None, workCode)), ("codeType", (None, 'json')), ("theme", (None, 'scratch')),("subtheme", (None, 'scratch')),("description", (None, description)),("fork", (None, fork)),("publish", (None,publish)),("thumbnail", (None, thumbnail)),("title", (None, title))]
                fields=urllib3.encode_multipart_formdata(fields=fields)
                body = fields[0]
                headers = headers
                headers['Content-Type'] = fields[1]
                response = self.client.post('https://icode.youdao.com/api/work/submit',data = body, headers = headers)
            else:
                if workType in ['Python', 'python']:
                    if save:
                        body = {
                            'code' : workCode,
                            'description' : description,
                            'title': title
                        }
                        headers = headers
                        headers['Content-Type'] = 'application/json'
                        response = self.client.post('https://icodeshequ.youdao.com/api/works/save', json = body, headers = headers)
                    else:
                        body = {
                            'code': workCode,
                            'description': description,
                            'title': title,
                            'imgUrl': thumbnail
                        }
                        headers = headers
                        headers['Content-Type'] = 'application/json'
                        response = self.client.post(f'https://icodeshequ.youdao.com/api/works/publish?publishType={publish}', json = body, headers = headers)
                else:
                    raise ValueError(f'The workType must be "Scratch" or "Python", not {workType}')
        else:
            if workType in ['Scratch', 'scratch']:
                fields = [("category", (None, 'lab')), ("code", (None, workCode)), ("codeType", (None, 'json')), ("theme", (None, 'scratch')),("subtheme", (None, 'scratch')),("description", (None, description)),("fork", (None, fork)),("publish", (None,publish)),("thumbnail", (None, thumbnail)),("title", (None, title)),('workid',(None,workId))]
                fields=urllib3.encode_multipart_formdata(fields=fields)
                body = fields[0]
                headers = headers
                headers['Content-Type'] = fields[1]
                response = self.client.post('https://icode.youdao.com/api/work/submit', data = body, headers = headers)
            elif workType in ['Python', 'python']:
                if save:
                    body = {
                        'code' : workCode,
                        'description' : description,
                        'title': title,
                        'id': workId
                    }
                    headers = headers
                    headers['Content-Type'] = 'application/json'
                    response = self.client.post('https://icodeshequ.youdao.com/api/works/save', json = body, headers = headers)
                else:
                    body = {
                        'code': workCode,
                        'description': description,
                        'title': title,
                        'imgUrl': thumbnail,
                        'id': workId
                    }
                    headers = headers
                    headers['Content-Type'] = 'application/json'
                    response = self.client.post(f'https://icodeshequ.youdao.com/api/works/publish?publishType={publish}', json = body, headers = headers)
            else:
                raise ValueError(f'The workType must be "Scratch" or "Python", not {workType}')

        result = response.json()
        return result
    
    def deleteWork(self, workId : str) -> dict:
        '''
        Delete a work.
        '''
        if not self.__loginStatus:
            raise LoginError('User is not logged in')
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        response = self.client.delete(f'https://icodeshequ.youdao.com/api/works/delete?id={workId}', headers = headers)
        reslut = response.json()
        return reslut
    
    def updateIntro(self, intro : str = 'IcodeAPI: The Best API Framework for icodeshequ.youdao.com in Python. Document url: https://xbz-studio.gitbook.io/icodeapi'):
        '''
        Update user intro.
        '''
        if not self.__loginStatus:
            raise LoginError('User is not logged in')
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        response = self.client.post('https://icodeshequ.youdao.com/api/user/updateIntro', data = intro.encode('utf-8'), headers = headers)
        result = response.json()
        return result
    
    def reply(self, content : str, commentId : int, replyId : int = None) -> dict:
        '''
        Reply a comment.

        You can reply a comment or an another reply.

        If you want to reply an another reply, you should 
        '''
        if not self.__loginStatus:
            raise LoginError('User is not logged in')
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        body = {'commentId': commentId,
                'content': content,
                'replyId': replyId}
        headers = headers
        headers['Content-Type'] = 'application/json'
        response = self.client.post('https://icodeshequ.youdao.com/api/works/reply', json = body, headers = headers)
        result = response.json()
        return result
    
    def deleteComment(self, commentId : int = None, replyId : int = None) -> dict:
        '''
        Delete a comment.
        '''
        if not self.__loginStatus:
            raise LoginError('User is not logged in')
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        if commentId:
            response = self.client.post(f'https://icodeshequ.youdao.com/api/works/comment/delete?commentId={commentId}', data = 'IcodeAPI delete comment'.encode('utf-8'), headers = headers)
        elif replyId:
            response = self.client.post(f'https://icodeshequ.youdao.com/api/works/reply/delete?replyId={replyId}', data = 'IcodeAPI delete reply'.encode('utf-8'), headers = headers)
        else:
            raise ValueError(f'Both commentId and replyId is None')
        result = response.json()
        return result
    
    def deleteMessage(self, messageId : int) -> dict:
        '''
        Delete a message in message hub.
        '''
        if not self.__loginStatus:
            raise LoginError('User is not logged in')
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        body = {
            'id': messageId
        }
        headers['Content-Type'] = 'application/json'
        response = self.client.post('https://icodeshequ.youdao.com/api/user/message/deleteComment', json = body, headers = headers)
        result = response.json()
        return result
    
    def uploadFile(self, name : str, suffix : str, file : Union[bytes, str]) -> dict:
        '''
        Upload file to icodeshequ.youdao.com .
        '''
        if not self.__loginStatus:
            raise LoginError('User is not logged in')
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        response = self.client.post(f'https://tiku-outside.youdao.com/nos/scratch/asset/{name}.{suffix}/', data = file, headers = headers)
        result = response.json()
        return result
    
    def praiseComment(self, commentId : int = None, replyId : int = None, mode : int = 1) -> dict:
        '''
        Praise a comment or reply.
        '''
        if not self.__loginStatus:
            raise LoginError('User is not logged in')
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        match mode:
            case 1:
                url = 'https://icodeshequ.youdao.com/api/works/comment/praise?'
            case 2:
                url = 'https://icodeshequ.youdao.com/api/works/comment/cancelPraise?'
            case _:
                raise ValueError(f'The mode must be 1 or 2, not {mode}')
        if commentId:
            url += f'commentId={commentId}'
        elif replyId:
            url = url.replace('comment', 'reply')
            url += f'replyId={replyId}'
        else:
            raise ValueError(f'Both commentId and replyId is None')
        response = self.client.post(url, data = 'IcodeAPI: praiseComment'.encode('utf-8'), headers = headers)
        result = response.json()
        return result
    
    def readMessage(self, messageId : int) -> dict:
        '''
        Read a message in messages hub.

        After reading, the message will not show a red point again.
        '''
        if not self.__loginStatus:
            raise LoginError('User is not logged in')
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        response = self.client.put(f'https://icodeshequ.youdao.com/api/user/message/read?id={messageId}', headers = headers)
        result = response.json()
        return result
    
    def readAllMessages(self, tab : int = 1) -> dict:
        '''
        Read all messages in messages hub.

        After reading, all messages will not show a red point again.

        tab = 1:
            Read all comment messages.
        tab = 2:
            Read all enshrine messages.
        tab = 3:
            Read all system messages.
        '''
        if not self.__loginStatus:
            raise LoginError('User is not logged in')
        headers = {'Cookie': self.__cookie, 'User-Agent': self.userAgent}
        headers['Content-Type'] = 'application/json'
        body = {
            "tab" : tab
        }
        response = self.client.post('https://icodeshequ.youdao.com/api/user/message/readAll', json = body, headers = headers)
        result = response.json()
        return result
    
    def __del__(self):
        self.client.close()
    
class AsyncIcodeAPI(IcodeAPI):
    '''
    Async version of IcodeAPI.

    AsyncIcodeAPI is a derived class of the IcodeAPI, but all APIs become asynchronous.

    Create a icodeshequ user.

    Go to https://icodeshequ.youdao.com to get your cookies.
    '''
    client : httpx.AsyncClient = None

    def __init__(self, cookie : str = '', userAgent : str = DEFAULT_USER_AGENT, httpxClient : httpx.AsyncClient = httpx.AsyncClient(), timeout : Union[float, int] = 10):
        self.__cookie = cookie.encode('utf-8')
        self.userAgent = userAgent
        self.client = httpxClient
        self.client.timeout = timeout

    async def login(self, newCookie : str = None) -> dict:
        '''
        Login to https://icodeshequ.youdao.com use self.__cookie.

        This function will return a dict, and the dict always be like:
        ```python
            {
                'encryptionUserId': str,
                'userId': str, 
                'name': str, 
                'image': str, 
                'permissions': list, 
                'mobile': str, 
                'hasCourse': bool, 
                'userIdentity': str,
                'courseType': str
            }
        ```
        '''
        if newCookie:
            self.__cookie = newCookie.encode('utf-8')
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        response = await self.client.get('https://icodecontest-online-api.youdao.com/api/user/info', headers = headers)
        if not (jsonres := response.json()).get('code'):
            result = jsonres.get('data')
            self.__loginStatus = True
        else:
            result = {}
            warnings.warn('Login failed', LoginWarning)
            self.__loginStatus = False
        self.__info = result
        return result
    
    def getLoginStatus(self):
        return self.__loginStatus
    
    def getInfo(self):
        return self.__info

    async def getWorkDetail(self, workId : str, addBrowseNum : bool = True) -> dict:
        '''
        Get work detail.

        This function will return a dict, and the dict always be like:
        ```python
        {
            'id': str, 
            'title': str, 
            'imgUrl': str, 
            'description': str,
            'type': int,
            'userId': str,
            'status': int,
            'likeNum': int,
            'browseNum': int,
            'enshrineNum': int,
            'code': str,
            'userName': str, 
            'userImage': str, 
            'haveLiked': bool ,
            'haveEnshrined': bool,
            'createTimeStr': str, 
            'updateTimeStr': str, 
            'codeLanguage': str, 
            'shortLink': str, 
            'theme': str, 
            'subTheme': str, 
            'iframeUrl': str, 
            'scratchFile': str, 
            'codeType': str, 
            'firstPopups': bool , 
            'forkAuthorizationStatus': bool, 
            'isFirstPublish': bool, 
            'haveReported': bool
        }
        ```
    '''
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        response = await self.client.get(f'https://icodeshequ.youdao.com/api/works/detail?id={workId}&addBrowseNum={str(addBrowseNum).lower()}', headers = headers)
        result = response.json().get('data')
        return result
    
    async def getWorkComments(self, workId : str, page : int = 1, getNum : int = 20) -> list:
        '''
        Get work comments.
        
        This function will return a list, and the list always be like:
        ```python
        [
            {
                'id': int, 
                'content': str, 
                'userId': str, 
                'name': str, 
                'image': str, 
                'isAuthor': bool, 
                'praiseNum': int, 
                'replyNum': int, 
                'time': int, 
                'hasPraised': bool
            }
        ]
        ```
        '''
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        response = await self.client.get(f'https://icodeshequ.youdao.com/api/works/comment/list?id={workId}&page={page}&size={getNum}', headers = headers)
        result = response.json().get('dataList')
        return result
    
    async def getMoreWorks(self, userId : str = None, workId : str = None) -> list:
        '''
        Get more works.

        This function will return a list, and the list always be like:
        ```python
        [
            {
                'id': str, 
                'title': str, 
                'imgUrl': str, 
                'likeNum': int, 
                'browseNum': int, 
                'userName': str, 
                'userImage': str
            }
        ]
        ```
        '''
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        if userId or workId:
            if userId == None:
                userId = await self.getWorkDetail(workId)
                userId = userId['userId']
                response = await self.client.get(f'https://icodeshequ.youdao.com/api/user/more_works/list?userId={userId}&currentWorksId=21a8bbf470ef4203abd549c641aac7a6', headers = headers)
                result = response.json().get('dataList')
            else:
                response = await self.client.get(f'https://icodeshequ.youdao.com/api/user/more_works/list?userId={userId}&currentWorksId=21a8bbf470ef4203abd549c641aac7a6', headers = headers)
                result = response.json().get('dataList')
            return result
        else:
            raise ValueError('Both userId and workId are None')
        
    async def getWorks(self, page : int = 1, getNum : int = 20, sortType : int = 2, theme : str = 'all', codeLanguage : str = 'all', keyword : Union[str, any] = '') -> list:
        '''
        Get works.
        
        Parameters
        ----------
        `page` : int, default 1
            Page number.
        `getNum` : int, default 20
            Number of works per page.
        `sortType` : int, default 1
            Sort type.

            1: Most likes

            2: Newest
        `theme` : str, default 'all'
            Work theme in icodeshequ.

            'all': All themes

            'play': Games theme

            'story': Story theme

            'art': Art theme

            'minecraft': Minecraft theme, the works about Minecraft

            'scratch': Scratch works

            'turtle': Python works
        `codeLanguage` : str, default 'all'
            The code language of works.

            'all': All code language

            'blockly': Blockly works

            'scratch': Scratch works

            'python': Python works
        `keyword` : str, default ''
            The key word of works.
        ----------

        This function will return a list, and the list always be like:
        ```python
            [
                {
                    'id': str, 
                    'title': str, 
                    'imgUrl': str, 
                    'userId': str, 
                    'browseNum': int, 
                    'userName': str, 
                    'userImage': str, 
                    'codeLanguage': str
                }
            ]
        ```
        '''
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        response = await self.client.get(f'https://icodeshequ.youdao.com/api/index/works/list?page={page}&size={getNum}&sortType={sortType}&theme={theme}&codeLanguage={codeLanguage}&keyword={keyword}', headers = headers)
        result = response.json().get('dataList')
        return result
    
    async def getMyWorks(self, page : int = 1, getNum : int = 20, theme : str = 'all', codeLanguage : str = 'all', status : int = 2, keyword : Union[str, any] = '') -> list:
        '''
        Get user works.

        Parameters
        ----------
        `page` : int, default 1
            Page number.
        `getNum` : int, default 20
            Number of works per page.
        `theme` : str, default 'all'
            Work theme in icodeshequ.

            'all': All themes

            'play': Games theme

            'story': Story theme

            'art': Art theme

            'minecraft': Minecraft theme, the works about Minecraft

            'scratch': Scratch works

            'turtle': Python works
        `codeLanguage` : str, default 'all'
            The code language of works.

            'all': All code language

            'blockly': Blockly works

            'scratch': Scratch works

            'python': Python works
        `status` : int, default 2
            The publishing status of works

            1: No published

            2: Published
        `keyword` : str, default ''
            The key word of works.
        ----------

        This function will return a list, and the list always be like:
        ```python
        [
            {
                'id': str, 
                'title': str, 
                'imgUrl': str, 
                'status': int,
                'likeNum': int, 
                'browseNum': int, 
                'enshrineNum': int, 
                'forkNum': int, 
                'userName': str, 
                'userImage': str, 
                'codeLanguage': str, 
                'theme': str, 
                'subTheme': str
            }
        ]
        ```
        '''
        if not self.__loginStatus:
            raise LoginError('User is not logged in')
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        response = await self.client.get(f'https://icodeshequ.youdao.com/api/user/works/list?page={page}&size={getNum}&status={status}&theme={theme}&codeLanguage={codeLanguage}&keyword={keyword}', headers = headers)
        result = response.json().get('dataList')
        return result
    
    async def getWorkSubmitInfo(self, workId : str) -> dict:
        '''
        Get work submit info.

        This function will return a dict, and the dict always be like:
        ```python
        {
            'avatar': str, 
            'category': str, 
            'codeType': str, 
            'commit': str, 
            'createtime': str, 
            'description': str, 
            'fork': int, 
            'forkcommit': str, 
            'forkfrom': str, 
            'likes': int, 
            'owner': str, 
            'publish': int, 
            'qrCodeImage': str, 
            'shareMessage': str, 
            'shareText': str, 
            'shareTitle': str, 
            'subtheme': str, 
            'theme': str, 
            'thumbnail': str, 
            'thumbnailList': list, 
            'title': str, 
            'username': str, 
            'visits': int, 
            'workid': str
        }
        ```

        When the work is a python work, the dict will be:
        ```python
        {
            'avatar': str, 
            'category': str, 
            'codeType': str, 
            'code': str,
            'commit': str, 
            'createtime': str, 
            'description': str, 
            'fork': int, 
            'forkcommit': str, 
            'forkfrom': str, 
            'likes': int, 
            'owner': str, 
            'publish': int, 
            'qrCodeImage': str, 
            'shareMessage': str, 
            'shareText': str, 
            'shareTitle': str, 
            'subtheme': str, 
            'theme': str, 
            'thumbnail': 'str, 
            'thumbnailList': list, 
            'title': str, 
            'username': str, 
            'visits': int, 
            'workid': str
        }
        ```
        '''
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        response = await self.client.get(f'https://icode.youdao.com/api/work/get?id={workId}', headers = headers)
        result = response.json()
        return result
    
    async def getPersonInfo(self, userId : str) -> dict:
        '''
        Get user info.

        The function will return a dict, and the dict always be like:
        ```python
        {
            'worksNum': int, 
            'viewNum': int, 
            'praiseNum': int, 
            'enshrinesNum': int, 
            'forkNum': int, 
            'userId': str, 
            'img': str, 
            'nickName': str, 
            'intro': str
        }
        ```
        '''
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        response = await self.client.get(f'https://icodeshequ.youdao.com/api/user/index/hisStatics?userId={userId}', headers = headers)
        result = response.json().get('data')
        return result

    async def getPersonWorks(self, userId : str, page : int = 1, getNum : int = 20) -> list:
        '''
        Get user works.

        This function will return a list, and the list always be like:
        ```
        [
            {
                'id': str, 
                'title': str, 
                'imgUrl': str, 
                'status': int, 
                'likeNum': int, 
                'browseNum': int, 
                'enshrineNum': int, 
                'forkNum': int, 
                'userName': str, 
                'userImage': str, 
                'codeLanguage': str, 
                'theme': str, 
                'subTheme': str
            }
        ]
        ```
        '''
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        response = await self.client.get(f'https://icodeshequ.youdao.com/api/user/works/hisWorksList?page={page}&size={getNum}&userId={userId}', headers = headers)
        result = response.json().get('dataList')
        return result

    async def getPersonEnshrines(self, userId : str, page : int = 1, getNum : int = 20) -> list:
        '''
        Get user enshrines.

        This function will return a list, and the list always be like:
        ```python
        [
            {
                'id': str, 
                'title': str, 
                'imgUrl': str, 
                'userId': str, 
                'status': int, 
                'likeNum': int, 
                'browseNum': int, 
                'userName': str, 
                'userImage': str, 
                'codeLanguage': str, 
                'theme': str, 
                'subTheme': str
            }
        ]
        ```
        '''
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        response = await self.client.get(f'https://icodeshequ.youdao.com/api/user/works/hisEnshrines?page={page}&size={getNum}&userId={userId}', headers = headers)
        result = response.json().get('dataList')
        return result
    
    async def getReplies(self, commentId : int, page : int = 1, getNum : int = 20) -> list:
        '''
        Get the replies of a comment.

        This function will return a list, and the list always be like:
        ```python
        [  # When this reply is a reply to a comment
            {
                "id": int,
                "content": str,
                "type": int,
                "commentId": int,
                "userId": str,
                "name": str,
                "image": str,
                "isAuthor": bool,
                "time": int,
                "praiseNum": int,
                "hasPraised": bool
            }
        ]
        [ # When this reply is a reply to an another reply
            {
                "id": int,
                "content": str,
                "type": int,
                "commentId": str,
                "userId": str,
                "name": str,
                "image": str,
                "isAuthor": bool,
                "replyUserId": str,
                "replyName": str,
                "replyImage": str,
                "time": int,
                "praiseNum": int,
                "hasPraised": bool
            }
        ]
        ```
        '''
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        response = await self.client.get(f'https://icodeshequ.youdao.com/api/works/reply/list?commentId={commentId}&page={page}&size={getNum}', headers = headers)
        result = response.json().get('dataList')
        return result
    
    async def getMessages(self, messageType : str = 'reply', page : int = 1, getNum : int = 20) -> list:
        '''
        Get the reply messages in messgaes hub.

        Parameters
        ----------
        `messageType` : str, default "reply"
            The type of messages in messages hub.

            "reply": reply message

            "enshrine": like and enshrine message

            "system": system message
        `page` : int, default 1
            Page number.
        `getNum` : int, default 20
            Number of works per page.
        ----------

        This function will return a list, and the list always be like:
        ```python
        [
            {
                'actionUserId': str,
                'actionUserImage': str,
                'actionUserName': str,
                'createTime': str,
                'createTimeStr': str,
                'haveRead': bool,
                'id': int,
                'type': int,
                'worksId': str,
                'worksTitle': str
            }
        ]
        ```
        '''
        headers = {
            'Cookie': self.__cookie,
            'User-Agent': self.userAgent}
        if not self.__loginStatus:
            raise LoginError('User is not logged in')
        match messageType:
            case 'reply':
                response = await self.client.get(f'https://icodeshequ.youdao.com/api/user/message/commentMessage?page={page}&size={getNum}', headers = headers)
            case 'enshrine':
                response = await self.client.get(f'https://icodeshequ.youdao.com/api/user/message/enshrinesMessage?page={page}&size={getNum}', headers = headers)
            case 'system':
                response = await self.client.get(f'https://icodeshequ.youdao.com/api/user/message/systemMessage?page={page}&size={getNum}', headers = headers)
            case _:
                raise ValueError(f'messageType must be "reply" or "enshrine" or "system", not {messageType}')
        result = response.json().get('dataList')
        return result

    async def getScratchAsset(self, md5ext : str):
        '''
        Get asset in scratch work.
        '''
        headers = {'User-Agent' : self.userAgent, 'Cookie' : self.__cookie}
        response = await self.client.get(f'https://ydschool-online.nosdn.127.net/svg/{md5ext}', headers = headers)
        result = response.content
        return result
    
    async def comment(self, workId : str, content : str) -> dict:
        '''
        Comment a work.
        '''
        if not self.__loginStatus:
            raise LoginError('User is not logged in')
        body = {
            'id': workId,
            'content': content
        }
        headers = {
            'Content-Type': 'application/json',
            'Cookie': self.__cookie,
            'User-Agent': self.userAgent}
        response = await self.client.post('https://icodeshequ.youdao.com/api/works/comment', json = body, headers = headers)
        result = response.json()
        return result
    
    async def like(self, workId : str, mode : int = 1) -> dict:
        '''
        Like a work.

        If mode = 1, like the work. If mode = 2, un-like the work.
        '''
        if not self.__loginStatus:
            raise LoginError('User is not logged in')
        headers = {'Cookie': self.__cookie, 'User-Agent': self.userAgent}
        url = f'https://icodeshequ.youdao.com/api/works/like?id={workId}&type={mode}'
        response = await self.client.post(url, data = 'IcodeAPI: Like request'.encode('utf-8'), headers = headers)
        result = response.json()
        return result
    
    async def enshrine(self, workId : str, mode : int = 1) -> dict:
        '''
        Enshrine a work.

        If mode = 1, enshrine the work. If mode = 2, un-enshrine the work.
        '''
        if not self.__loginStatus:
            raise LoginError('User is not logged in')
        headers = {'Cookie': self.__cookie, 'User-Agent': self.userAgent}
        urlContent = 'enshrine' if (not (mode - 1)) else 'cancelEnshrine'
        url = f'https://icodeshequ.youdao.com/api/user/works/{urlContent}?worksId={workId}'
        response = await self.client.post(url, data = 'IcodeAPI: Enshrine request'.encode('utf-8'), headers = headers)
        result = response.json()
        return result
    
    async def report(self, workId : str, reason : str, reportType : int) -> dict:
        '''
        Report a work.

        reportType:
            1: plagiarize,
            2: ad spam,
            3: personal attacks,
            4: illegal,
            5: r18 / r18g
        '''
        if not self.__loginStatus:
            raise LoginError('User is not logged in')
        headers = {'Cookie': self.__cookie, 'User-Agent': self.userAgent}
        body = {'worksIdStr':workId,
                'category':reportType,
                'description':reason
                }
        response = await self.client.post('https://icodeshequ.youdao.com/api/works/report', json = body, headers = headers)
        result = response.json()
        return result
    
    async def submitWork(self, workCode : str = '', 
                   workType : str = 'Scratch', 
                   publish : int = 1,
                   save : int = False,
                   title : str = 'Scratch Project', 
                   description : str = 'Project Description', 
                   thumbnail : str = 'http://ydschool-online.nosdn.127.net/svg/0c3a986d5266bd5a186014aebd219e05c9696de777dea2b5dfe658dc661e572c.png',
                   fork : int = 0,
                   workDetail : tuple = None,
                   workId : str = None) -> dict:
        '''
        Submit a work.

        This function only supported to submit Scratch or Python work, no Blockly.

        If the workId isnt None, the function will reSubmit the work.

        When the workType is Python, and the save is true, the funciton will only save the work, not publish the work.

        If publish = 1, the function will publish the work, when it is 2, the fucntion will unpublish the work.

        If fork = 1, allow others to fork your work, if fork = 0, dont allow others to fork your work.

        If workDetail should be a tuple. workDetail[0] = `getWorkDetail()` return value, workDetail[1] = `getWorkSubmitInfo()` return value.
        '''
        if not self.__loginStatus:
            raise LoginError('User is not logged in')
        headers = {'Cookie': self.__cookie, 'User-Agent': self.userAgent}
        if workDetail:
            if not workId:
                match workDetail[0].get('codeLanguage'):
                    case 'scratch':
                        fields = {
                            'category' : 'lab',
                            'code' : workDetail[0].get('code'),
                            'codeType' : 'json',
                            'theme' : 'scratch',
                            'subtheme' : 'scratch',
                            'description' : workDetail[0].get('description'),
                            'fork' : workDetail[1].get('fork'),
                            'publish' : workDetail[0].get('status') % 2 + 1,
                            'thumbnail' : workDetail[0].get('imgUrl'),
                            'title' : workDetail[0].get('title')
                        }
                        fields=urllib3.encode_multipart_formdata(fields=fields)
                        body = fields[0]
                        headers = headers
                        headers['Content-Type'] = fields[1]
                        response = await self.client.post('https://icode.youdao.com/api/work/submit',data = body, headers = headers)
                    case 'python':
                        if save:
                            body = {
                                'code' : workDetail[0].get('code'),
                                'description' : workDetail[0].get('description'),
                                'title': workDetail[0].get('title')
                            }
                            headers = headers
                            headers['Content-Type'] = 'application/json'
                            response = await self.client.post('https://icodeshequ.youdao.com/api/works/save', json = body, headers = headers)
                        else:
                            body = {
                                'code' : workDetail[0].get('code'),
                                'description' : workDetail[0].get('description'),
                                'title': workDetail[0].get('title'),
                                'imgUrl': workDetail[0].get('imgUrl')
                            }
                            headers = headers
                            headers['Content-Type'] = 'application/json'
                            response = await self.client.post(f'https://icodeshequ.youdao.com/api/works/publish?publishType={workDetail[0].get("status") % 2 + 1}', json = body, headers = headers)
                    case _:
                        raise ValueError('Invalid workDetail.')
            else:
                match workDetail[0].get('codeLanguage'):
                    case 'scratch':
                        fields = {
                            'category' : 'lab',
                            'code' : workDetail[0].get('code'),
                            'codeType' : 'json',
                            'theme' : 'scratch',
                            'subtheme' : 'scratch',
                            'description' : workDetail[0].get('description'),
                            'fork' : workDetail[1].get('fork'),
                            'publish' : workDetail[0].get('status') % 2 + 1,
                            'thumbnail' : workDetail[0].get('imgUrl'),
                            'title' : workDetail[0].get('title'),
                            'workid' : workId
                        }
                        fields=urllib3.encode_multipart_formdata(fields=fields)
                        body = fields[0]
                        headers = headers
                        headers['Content-Type'] = fields[1]
                        response = await self.client.post('https://icode.youdao.com/api/work/submit',data = body, headers = headers)
                    case 'python':
                        if save:
                            body = {
                                'code' : workDetail[0].get('code'),
                                'description' : workDetail[0].get('description'),
                                'title': workDetail[0].get('title'),
                                'id' : workId
                            }
                            headers = headers
                            headers['Content-Type'] = 'application/json'
                            response = await self.client.post('https://icodeshequ.youdao.com/api/works/save', json = body, headers = headers)
                        else:
                            body = {
                                'code' : workDetail[0].get('code'),
                                'description' : workDetail[0].get('description'),
                                'title': workDetail[0].get('title'),
                                'imgUrl': workDetail[0].get('imgUrl'),
                                'id' : await workId
                            }
                            headers = headers
                            headers['Content-Type'] = 'application/json'
                            response = await self.client.post(f'https://icodeshequ.youdao.com/api/works/publish?publishType={workDetail[0].get("status") % 2 + 1}', json = body, headers = headers)
                    case _:
                        raise ValueError('Invalid workDetail.')
            result = response.json()
            return result
        if not workId:
            if workType in ['Scratch', 'scratch']:
                fields = [("category", (None, 'lab')), ("code", (None, workCode)), ("codeType", (None, 'json')), ("theme", (None, 'scratch')),("subtheme", (None, 'scratch')),("description", (None, description)),("fork", (None, fork)),("publish", (None,publish)),("thumbnail", (None, thumbnail)),("title", (None, title))]
                fields=urllib3.encode_multipart_formdata(fields=fields)
                body = fields[0]
                headers['Content-Type'] = fields[1]
                response = await self.client.post('https://icode.youdao.com/api/work/submit', data = body, headers = headers)
            else:
                if workType in ['Python', 'python']:
                    if save:
                        body = {
                            'code' : workCode,
                            'description' : description,
                            'title': title
                        }
                        headers['Content-Type'] = 'application/json'
                        response = await self.client.post('https://icodeshequ.youdao.com/api/works/save', json = body, headers = headers)
                    else:
                        body = {
                            'code': workCode,
                            'description': description,
                            'title': title,
                            'imgUrl': thumbnail
                        }
                        headers['Content-Type'] = 'application/json'
                        response = await self.client.post(f'https://icodeshequ.youdao.com/api/works/publish?publishType={publish}', json = body, headers = headers)
                else:
                    raise ValueError(f'The workType must be "Scratch" or "Python", not {workType}')
        else:
            if workType in ['Scratch', 'scratch']:
                fields = [("category", (None, 'lab')), ("code", (None, workCode)), ("codeType", (None, 'json')), ("theme", (None, 'scratch')),("subtheme", (None, 'scratch')),("description", (None, description)),("fork", (None, fork)),("publish", (None,publish)),("thumbnail", (None, thumbnail)),("title", (None, title)),('workid',(None,workId))]
                fields=urllib3.encode_multipart_formdata(fields=fields)
                body = fields[0]
                headers['Content-Type'] = fields[1]
                response = await self.client.post('https://icode.youdao.com/api/work/submit', data = body, headers = headers)
            elif workType in ['Python', 'python']:
                if save:
                    body = {
                        'code' : workCode,
                        'description' : description,
                        'title': title,
                        'id': workId
                    }
                    headers['Content-Type'] = 'application/json'
                    response = await self.client.post('https://icodeshequ.youdao.com/api/works/save', json = body, headers = headers)
                else:
                    body = {
                        'code': workCode,
                        'description': description,
                        'title': title,
                        'imgUrl': thumbnail,
                        'id': workId
                    }
                    headers['Content-Type'] = 'application/json'
                    response = await self.client.post(f'https://icodeshequ.youdao.com/api/works/publish?publishType={publish}', data = body, headers = headers)
            else:
                raise ValueError(f'The workType must be "Scratch" or "Python", not {workType}')

        result = response.json()
        return result
    
    async def deleteWork(self, workId : str) -> dict:
        '''
        Delete a work.
        '''
        if not self.__loginStatus:
            raise LoginError('User is not logged in')
        headers = {'Cookie' : self.__cookie, 'User-Agent' : self.userAgent}
        response = await self.client.delete(f'https://icodeshequ.youdao.com/api/works/delete?id={workId}', headers = headers)
        reslut = response.json()
        return reslut
    
    async def updateIntro(self, intro : str = 'IcodeAPI: The Best API Framework for icodeshequ.youdao.com in Python. Document url: https://xbz-studio.gitbook.io/icodeapi'):
        '''
        Update user intro.
        '''
        if not self.__loginStatus:
            raise LoginError('User is not logged in')
        headers = {'Cookie' : self.__cookie, 'User-Agent' : self.userAgent}
        response = await self.client.post('https://icodeshequ.youdao.com/api/user/updateIntro', data = intro.encode('utf-8'), headers = headers)
        result = response.json()
        return result
    
    async def reply(self, content : str, commentId : int, replyId : int = None) -> dict:
        '''
        Reply a comment.

        You can reply a comment or an another reply.

        If you want to reply an another reply, you should 
        '''
        if not self.__loginStatus:
            raise LoginError('User is not logged in')
        body = {'commentId': commentId,
                'content': content,
                'replyId': replyId}
        headers = {'Cookie' : self.__cookie, 'User-Agent' : self.userAgent}
        headers['Content-Type'] = 'application/json'
        response = await self.client.post('https://icodeshequ.youdao.com/api/works/reply', json = body, headers = headers)
        result = response.json()
        return result
    
    async def deleteComment(self, commentId : int = None, replyId : int = None) -> dict:
        '''
        Delete a comment.
        '''
        if not self.__loginStatus:
            raise LoginError('User is not logged in')
        headers = {'Cookie' : self.__cookie, 'User-Agent' : self.userAgent}
        if commentId:
            response = await self.client.post(f'https://icodeshequ.youdao.com/api/works/comment/delete?commentId={commentId}', data = 'IcodeAPI delete comment'.encode('utf-8'), headers = headers)
        elif replyId:
            response = await self.client.post(f'https://icodeshequ.youdao.com/api/works/reply/delete?replyId={replyId}', data = 'IcodeAPI delete reply'.encode('utf-8'), headers = headers)
        else:
            raise ValueError(f'Both commentId and replyId is None')
        result = response.json()
        return result
    
    async def deleteMessage(self, messageId : int) -> dict:
        '''
        Delete a message in message hub.
        '''
        if not self.__loginStatus:
            raise LoginError('User is not logged in')
        headers = {'Cookie' : self.__cookie, 'User-Agent' : self.userAgent}
        body = {
            'id': messageId
        }
        headers['Content-Type'] = 'application/json'
        response = await self.client.post('https://icodeshequ.youdao.com/api/user/message/deleteComment', json = body, headers = headers)
        result = response.json()
        return result
    
    async def uploadFile(self, name : str, suffix : str, file : Union[bytes, str]) -> dict:
        '''
        Upload file to icodeshequ.youdao.com .
        '''
        if not self.__loginStatus:
            raise LoginError('User is not logged in')
        headers = {'Cookie': self.__cookie, 'User-Agent': self.userAgent}
        response = await self.client.post(f'https://tiku-outside.youdao.com/nos/scratch/asset/{name}.{suffix}/', data = file)
        result = response.json()
        return result
    
    async def praiseComment(self, commentId : int = None, replyId : int = None, mode : int = 1) -> dict:
        '''
        Praise a comment or reply.
        '''
        if not self.__loginStatus:
            raise LoginError('User is not logged in')
        match mode:
            case 1:
                url = 'https://icodeshequ.youdao.com/api/works/comment/praise?'
            case 2:
                url = 'https://icodeshequ.youdao.com/api/works/comment/cancelPraise?'
            case _:
                raise ValueError(f'The mode must be 1 or 2, not {mode}')
        if commentId:
            url += f'commentId={commentId}'
        elif replyId:
            url = url.replace('comment', 'reply')
            url += f'replyId={replyId}'
        else:
            raise ValueError(f'Both commentId and replyId is None')
        headers = {'Cookie': self.__cookie, 'User-Agent': self.userAgent}
        response = await self.client.post(url, data = 'IcodeAPI: praiseComment'.encode('utf-8'), headers = headers)
        result = response.json()
        return result
    
    async def readMessage(self, messageId : int) -> dict:
        '''
        Read a message in messages hub.

        After reading, the message will not show a red point again.
        '''
        if not self.__loginStatus:
            raise LoginError('User is not logged in')
        headers = {'Cookie': self.__cookie, 'User-Agent': self.userAgent}
        response = await self.client.put(f'https://icodeshequ.youdao.com/api/user/message/read?id={messageId}', headers  = headers)
        result = response.json()
        return result
    
    async def readAllMessages(self, tab : int = 1) -> dict:
        '''
        Read all messages in messages hub.

        After reading, all messages will not show a red point again.

        tab = 1:
            Read all comment messages.
        tab = 2:
            Read all enshrine messages.
        tab = 3:
            Read all system messages.
        '''
        if not self.__loginStatus:
            raise LoginError('User is not logged in')
        headers = {'Cookie': self.__cookie, 'User-Agent': self.userAgent}
        headers['Content-Type'] = 'application/json'
        body = {
            "tab" : tab
        }
        response = await self.client.post('https://icodeshequ.youdao.com/api/user/message/readAll', json = body, headers = headers)
        result = response.json()
        return result

    
    async def closeClient(self):
        '''
        Close the client.
        '''
        await self.client.aclose()

    def __del__(self):
        pass

def getWorkIdFromUrl(url : str) -> str:
    '''
    Get work id from url.
    '''
    try:
        parsedUrl = urllib.parse.urlparse(url)[2].split('/')[2]
        return parsedUrl
    except:
        raise ValueError('Invalid URL.')

def getUserIdFromUrl(url : str) -> str:
    '''
    Get user id from url.
    '''
    try:
        result = url[url.index('=')+1::]
        return result
    except:
        raise ValueError('Invalid URL.')
        
'''
Update Log

alpha阶段:
    0.1 
        增加IcodeAPI类,
        增加api
    0.2 
        增加了api,
        添加了参数错误报错
    0.3 
        增加了2个api,
        把getInfo改成了login,
        优化了些内容
    0.3.1 
        修复bug,
        加了一个api
    0.4 
        增加了2个api,
        增加了用户登录警告和未登录报错,
        优化了getWorkIdFromUrl方法,
        添加了icodeapi的loginStatus成员,
        修改了icodeapi中info成员的内容
    0.5 
        增加了3个api
    0.6 
        增加了2个api,
        修复了getWorkComments的bug,
        优化了一些内容
alpha阶段结束
beta阶段:
    0.1 
        增加AsyncIcodeAPI类,作为IcodeAPI的派生类.
        不再使用aiohttp,改用httpx实现对异步的支持,
        优化了一些内容
    0.2 
        完成所有异步API,
        移除了IcodeAPI的headers成员,
        增加LoginWarning,
        增加一个api
    0.3 
        将IcodeAPI的urllib3Client更换为httpxClient,全面开始使用httpx连接池,
        修复了4~5个大大小小的bug,
        添加了IcodeAPI中readAllMessages的注释,
        添加IcodeAPI和AsyncIcodeAPI的submitWork的fork参数,
        优化部分代码
beta阶段结束
正式版：
    v1.0.0
        添加IcodeAPI和AsyncIcodeAPI的timeout参数,
        增加getScratchAsset函数以获取scratch作品资源,
        增加getUserIdFromUrl函数,
        增加icodeapi.tools模块封装一些实用工具,
        修复3~4个bug,给submitWork添加workDetail参数,添加workCode参数默认值,且workType现在允许"scratch"和"python"这样的写法,
        给getWorkDetail增加了addBrowseNum参数,优化了部分代码
    v1.0.1
        给tools模块增加了CommentsCleaner方法,用于异步清理评论,
        改进tools模块的DownloadWork方法,现在它可以下载codeLanguage为"python"的作品,且在识别到不支持的codeLanguage时会抛出TypeError错误,
        改进tools模块的所有方法,现在临时生成的AsyncIcodeAPI会自动执行closeClient方法,
        给tools模块的ViewNumMaker方法添加了进度提示,
        修复了AsyncIcodeAPI中getMyWorks方法参数填入错误的bug,
        现在IcodeAPI和AsyncIcodeAPI的cookie, info, loginStatus均改为私有成员,添加了同步方法getInfo和getLoginStatus让用户获取他们,
        添加IcodeAPI和AsyncIcodeAPI中login方法的newCookie参数,使一个账号对象可以进行重登录
        添加常量DEFAULT_USER_AGENT,
        优化注释
'''