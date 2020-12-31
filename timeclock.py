import time,os,pickle
def moneyfmt(x): return "${:,.2f}".format(x)+''
def timefmt(hours):
	out=[]
	s=hours*60*60
	names=[['month',730.001*60*60],['week',7*24*60*60],['day',24*60*60],['hour',60*60],['minute',60],['second',1]]
	while names and s>= 0:
		cur=names.pop(0)
		if s<cur[1]:continue
		
		if s//cur[1] >1: cur[0]+='s'
		
		out.append(str(int(s//cur[1])) +' '+cur[0])
		s %= cur[1]
	return ', '.join(out)
class punch:
	def __init__(self,headingin):
		self.headingin=headingin
		self.ts=time.time()
	def __repr__(self):
		return ['clocked in','clocked out'][not self.headingin]+': '+time.ctime(self.ts)
class day:
	def __init__(self):
		self.punches=list()
	def estimate(self):
		out=0
		try: old=self.punches[0]
		except: return 0
		for x in self.punches:
			if not x.headingin and old.headingin:
				out += x.ts-old.ts
			old=x
		if old.headingin:
			out+=time.time()-old.ts
		return out/60/60
	def add(self,headingin):
		self.punches.append(punch(headingin))
	def delete(self,index):
		del self.punches[index]
	def pop(self):
		return self.punches.pop()
	def __repr__(self):
		pchs='\n'.join([' ['+str(c)+'] '+str(x) for c,x in enumerate(self.punches)])
		return '[\n'+pchs+'\n]'+str(timefmt(self.estimate()))

payrate=12*1.05
taxrate=597.97/700.46
target='timeclock_history'
root='/storage/emulated/0/'
file=os.path.join(root,target)
hist=day()
if os.path.isfile(file):
	hist=pickle.load(open(file,"rb"))
def save():
	pickle.dump(hist,open(file,'wb'))
	print('saved to',file)
while(True):
	print('-'*60)
	print(hist)
	first,last=(hist.punches[0].ts,hist.punches[len(hist.punches)-1].ts)
	print(' {:,.2f}'.format(hist.estimate()),'hrs')
	print(' '+moneyfmt(taxrate*hist.estimate()*payrate))
	print(' over a period of: '+timefmt(round((last-first)/60/60)))
	i=input('\n\ncontrol codes:\n c to clockin/out, or\n s to save, or\n d to delete a timestamp\n u to remove newest timestamp\n delfile to delete save file: ')
	i=i.lower().strip()
	if i=='c':
		gin=input('clock in? (y/n): ').lower().strip()
		gin={'y':True,'n':False}[gin]
		hist.add(gin)
	elif i=='s':
		save()
	elif i=='d':
		n=input('\nenter index to delete: ')
		hist.delete(int(n))
	elif i=='u':
		hist.pop()
	elif i=='delfile':
		try:
			os.remove(file)
		except:
			print('error thrown for file deletion')