# -*- coding: utf-8 -*-
import time,json,base64,hmac,hashlib,requests
import os,sys
sys.path.append('.')
sys.path.append('..')
import const
cf=const.createFile


##秘钥
AccessKey = '4144791d6ba8303982b6c7b2cb963e693304e3d9'
SecretKey = 'c0499802d3947cf3e765decedc767d15c1155a2b'

##预设变量，也可通过相册API获取


def tob(args):
	return bytes(args,encoding='utf=8')
def tos(b):
	return b.decode(encoding='utf-8')
def getDDL():
	return int(time.time())+ 60
def getULparam(config):
	aid=config['aid']
	httptype = config['httptype']
	fr = config['ul_from']
	return { "deadline": getDDL(), "from": fr, "aid":aid, "httptype":httptype}

album_id = 1334486
album_pages = 1

simple_par={ "deadline": getDDL(), "from": "file", "aid":album_id, "httptype":1}
# simple_par={ "deadline": deadline, "action": "album", "aid":album_id, "page_no":1}

def getToken(config):
	jsoncode = json.dumps(getULparam(config)).replace(' ','')
	# print(jsoncode)	# "deadline=1501001316&from=web&aid=1334486&httptype=1"
	encodedParam = base64.b64encode(tob(jsoncode))
	sign = hmac.new(tob(config['SECRETKEY']), encodedParam, digestmod=hashlib.sha1).hexdigest()
	# print(sign)  ce207b4e00cce93a1e0396fae637ac43c38640b0
	encodedSign = base64.b64encode(tob(sign))
	Token = config['ACCESSKEY'] + ':' + tos(encodedSign) + ':' + tos(encodedParam)
	return Token

def uppic(dirpath,file, Token,config):
	"""
	Upload one pic, return the result don't haddle error
	@filepath the path to pic

	"""
	upurl = config['upurl']
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

def reuploadFailed(suc,fail,config):
	for k in fail.keys():
		if not os.path.exists(k):
			del fail[k]
		else:
			h,t=os.path.split(k)
			di=uppic(h,t,getToken(config),config)
			if not 'code' in di:
				di['updatetime'] = time.time() # used to calc if we need up it again
				suc.update({k:di})
				del fail[k]

def uppics(dirpath,files,config):
	"""
	Take a list of filepath, use params to calculate token
	up load all pics to one album, 
	Return return info(dicts)
	"""

	Token = getToken(config)

	success = {}
	failure = {}
	params=getULparam(config)
	print(dirpath,files)
	for file in files:
		di=uppic(dirpath,file,Token,config)
		if not 'code' in di:
			di['updatetime'] = time.time() # used to calc if we need up it again
			success.update({dirpath+file:di})
		else:
			failure.update({dirpath+file:di})
	return success,failure

	

def getPicsFromDir(dirpath,config):
	"""return files ending with pic extensions"""
	l= os.listdir(dirpath)
	return [m for m in l if m[m.rfind(".")+1:].lower() in config['SUFFIX_LIST'].split(',')]


def getMdPics(result):
	d = result.copy()
	for k in d.keys():
		v=d.get(k)
		d.update({k:v['markdown'].replace("Markdown",k)})
	return d




if __name__ == '__main__':
	cf('success.json',initial="{}")
	cf('failure.json',initial="{}")
	cf('config.json',initial="{}")
	with open("success.json", "r") as f:
		suc = json.load(f)
	with open("failure.json", "r") as f:
		fail = json.load(f)
	with open("config.json", "r") as f:
		config = json.load(f)

	l=len(sys.argv)
	go=0
	if l==1:
		print('No dir to upload. Specify it.\nEg.: python3 pver.py /home/')
		exit(1)
	elif l==2:
		if not os.path.exists(sys.argv[1]):
			print('dir Not Found')
			exit(1)
		elif not os.path.isdir(sys.argv[1]):
			print('Not a dir')
			exit(1)
		else:
			go=1
	if not go:
		print("Something wrong happens. Bye.")
		exit(1)
	reuploadFailed(suc,fail,config)
	dirp = sys.argv[1]
	if dirp[-1]!='/':
		dirp+="/"
	cur_suc,cur_fail = uppics(dirp, getPicsFromDir(dirp,config), config)
	suc.update(cur_suc)
	fail.update(cur_fail)
	print()


	print(getMdPics(suc))
	with open("success.json","w") as f:
		json.dump(suc,f,indent=4)
	with open("failure.json","w") as f:
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