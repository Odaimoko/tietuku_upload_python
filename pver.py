# -*- coding: utf-8 -*-
import time,json,base64,hmac,hashlib,requests
import os,sys
from functools import wraps
sys.path.append('.')
sys.path.append('..')
import const
cf=const.createFile

SUFFIX_LIST = ['png','gif','jpg','jpeg']

##秘钥
AccessKey = '4144791d6ba8303982b6c7b2cb963e693304e3d9'
SecretKey = 'c0499802d3947cf3e765decedc767d15c1155a2b'

##预设变量，也可通过相册API获取
album_id = 1334486;
album_pages = 1;

upurl="http://up.imgapi.com/"
deadline = int(time.time())+ 60
simple_par={ "deadline": deadline, "from": "file", "aid":album_id, "httptype":1}
# simple_par={ "deadline": deadline, "action": "album", "aid":album_id, "page_no":1}


def tob(args):
	return bytes(args,encoding='utf=8')
def tos(b):
	return b.decode(encoding='utf-8')



def getToken(param):
	jsoncode = json.dumps(simple_par).replace(' ','')
	# print(jsoncode)	# "deadline=1501001316&from=web&aid=1334486&httptype=1"
	encodedParam = base64.b64encode(tob(jsoncode))
	sign = hmac.new(tob(SecretKey), encodedParam, digestmod=hashlib.sha1).hexdigest()
	# print(sign)  ce207b4e00cce93a1e0396fae637ac43c38640b0
	encodedSign = base64.b64encode(tob(sign))
	Token = AccessKey + ':' + tos(encodedSign) + ':' + tos(encodedParam)
	return Token

def uppic(dirpath,file, Token):
	"""
	Upload one pic, return the result don't haddle error
	@filepath the path to pic

	"""
	filepath = dirpath + file
	tkpar = {"Token": Token}
	filetype = filepath[filepath.rfind(".") + 1:]
	if filetype == 'jpg':
		filetype = 'jpeg'

	tkpar.update({"type": "image/" + filetype})
	tkpar.update({"name": file})
	with open(filepath, "rb") as f:
		con = f.read()
	multiple_files = [('file', ('a', con, 'image/' + filetype))]
	di = {}
	try:
		responesss = requests.post(upurl, data=tkpar, files=multiple_files)
		t = responesss.text
		di = json.loads(t)
		if not 'code' in di:
			print(filepath, "\tUL successfully.")
		else:
			print(filepath, 'UL failed.')

	except:
		print(filepath, 'UL failed.')
	finally:
		return di

def reuploadFailed(suc,fail):
	for k in fail.keys():
		if not os.path.exists(k):
			del fail[k]
		else:
			h,t=os.path.split(k)
			di=uppic(h,t,getToken(simple_par))
			if not 'code' in di:
				di['updatetime'] = time.time() # used to calc if we need up it again
				suc.update({k:di})
				del fail[k]

def uppics(dirpath,files,params):
	"""
	Take a list of filepath, use params to calculate token
	up load all pics to one album, 
	Return return info(dicts)
	"""

	Token = getToken(params)

	success = {}
	failure = {}
	print(dirpath,files,params)
	for file in files:
		di=uppic(dirpath,file,Token)
		if not 'code' in di:
			di['updatetime'] = time.time() # used to calc if we need up it again
			success.update({dirpath+file:di})
		else:
			failure.update({dirpath+file:di})
	return success,failure

	

def getPicsFromDir(dirpath):
	"""return files ending with pic extensions"""
	l= os.listdir(dirpath)
	return [m for m in l if m[m.rfind(".")+1:].lower() in SUFFIX_LIST]
def getMdPics(result):
	d = result.copy()
	for k in d.keys():
		v=d.get(k)
		d.update({k:v['markdown'].replace("Markdown",k)})
	return d




if __name__ == '__main__':
	cf('success.json')
	cf('fail.json')

	with open("success.json", "r") as f:
		suc = json.load(f)
	with open("fail.json", "r") as f:
		fail = json.load(f)
	print(suc, fail)
	reuploadFailed(suc,fail)
	dirp = '/Users/oda/Desktop/an/'
	cur_suc,cur_fail = uppics(dirp,getPicsFromDir(dirp), simple_par)
	suc.update(cur_suc)
	fail.update(cur_fail)
	print()


	print(getMdPics(suc))
	with open("success.json","w") as f:
		json.dump(suc,f,indent=4)
	with open("fail.json","w") as f:
		json.dump(fail,f,indent=4)

"""
# for page in range(1,album_pages+1):
#     ##请求参数和URL
#     deadline = int(time.time())+ 60
#     tmp_params={ "deadline": deadline, "action": "album", "aid":album_id, "page_no":page}

#     ##请求参数与秘钥生成Token
#     jsoncode = json.dumps(tmp_params)
#     encodedParam = base64.b64encode(jsoncode)
#     sign = hmac.new(SecretKey, encodedParam, digestmod=hashlib.sha1).hexdigest()
#     encodedSign = base64.b64encode(sign)
#     Token = AccessKey + ':' + encodedSign + ':' + encodedParam

#     ##发送http请求
#     parameters = {"Token": Token}
#     data = urllib.urlencode(parameters)
#     request=urllib2.Request(url,data)
#     response=urllib2.urlopen(request)

#     res_data = response.read()
#     res_dict=json.loads(res_data)

#     for e in res_dict["pic"]:
#         result = result + e["name"]+" : "+"\""+e["linkurl"]+"\"" +",\n"

# print result
"""