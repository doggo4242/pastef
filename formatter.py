import subprocess

def format(code,ext):
	# clang-format languages
	clang = ['c','cpp','java','cs','objc','protobuf','objectivec','csharp','c++','h','hpp','pb','obj-c']
	# prettier languages
	prettier = ['js','javascript','ts','typescript','css','html','json','yaml','jsx','php']
	# single-purpose formatters
	cmds = {'kt':['ktlint','--stdin','-F'],'kotlin':['ktlint','--stdin','-F'],
		'py':'yapf','python':'yapf','rs':'rustfmt','rust':'rustfmt',
		'hs':'ormolu','haskell':'ormolu','lua':'lua-format',
		'x86asm':'asmfmt','armasm':'asmfmt','go':'gofmt',
		'rb':'rufo','ruby':'rufo'}
	cmd = cmds.get(ext)
	if ext in clang:
		cmd='clang-format'
	elif ext in prettier or ext[:3] == 'php':
		if ext == 'js' or ext == 'javascript' or ext == 'jsx':
			ext='babel'
		elif ext == 'ts':
			ext='typescript'
		elif ext[:3] == 'php': # deal with php versions
			ext='php'
		cmd=['npx', 'prettier','--parser',ext]
	elif cmd == None:
		# not supported, return plain code
		return code
	# run the formatter
	res=subprocess.Popen(cmd,stdout=subprocess.PIPE,stdin=subprocess.PIPE)
	# send code to stdin
	res=res.communicate(input=code.encode('utf-8'))[0]
	return res
