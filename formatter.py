import subprocess

def bstr_to_str(str_lst):
	final=[]
	for i in str_lst:
		final.append(i.decode('utf-8'))
	return ''.join(final)

def format(code,ext):
#	code=code.replace('\'','\\\'')
	clang = ['c','cpp','java','cs','objc','protobuf']
	prettier = ['js','javascript','ts','typescript','css','html','json','yaml','jsx','php']
	cmd = None
	if ext in clang:
		cmd='clang-format'
	elif ext in prettier:
		if ext == 'js' or ext == 'javascript' or ext == 'jsx':
			ext='babel'
		elif ext == 'ts':
			ext='typescript'
		cmd=['npx', 'prettier','--parser',ext]
	elif ext == 'kt' or ext == 'kotlin':
		cmd=['ktlint','--stdin','-F']
	elif ext == 'py' or ext == 'python':
		cmd='yapf'
	elif ext == 'rs' or ext == 'rust':
		cmd='rustfmt'
	elif ext == 'hs' or ext == 'haskell':
		cmd='ormolu'
	elif ext == 'lua':
		cmd='lua-format'
	elif ext == 'x86asm' or ext == 'armasm':
		cmd='asmfmt'
	elif ext == 'go':
		cmd='gofmt'
	elif ext == 'rb' or ext == 'ruby':
		cmd='rufo'
	else:
		print('exiting')
		return code
	res=subprocess.Popen(cmd,stdout=subprocess.PIPE,stdin=subprocess.PIPE)
	res=res.communicate(input=code.encode('utf-8'))[0]
	return res
