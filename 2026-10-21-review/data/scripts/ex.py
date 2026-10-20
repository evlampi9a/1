# usage: python3 ex.py <tool-result-file> <out-name> [--daily]
import json,sys,os
f,out=sys.argv[1],sys.argv[2]
raw=open(f).read()
try:
    o=json.loads(raw)
except Exception:
    o=None
if isinstance(o,list): t=json.loads(o[0]['text'])
elif isinstance(o,dict) and 'content' in o: t=json.loads(o['content'][0]['text'])
else: t=o
d=t['data']; j=d['jsonResponse']
names=[m.get('segment') for m in j['seriesMetadata']]
res={'title':t.get('title'),'x':j.get('xValuesForTimeSeries'),'series':{}}
for i,n in enumerate(names):
    key=n if n not in res['series'] else f"{n}#{i}"
    ov=j['overallSeries'][i][0]['value'] if j.get('overallSeries') and i<len(j['overallSeries']) else None
    ts=[p['value'] for p in j['timeSeries'][i]] if j.get('timeSeries') and i<len(j['timeSeries']) else None
    res['series'][key]={'overall':ov,'daily':ts,'meta':j['seriesMetadata'][i] if i<len(j['seriesMetadata']) else None}
res['definition']=t.get('definition') or d.get('definition')
os.makedirs('/home/user/1/2026-10-21-review/data/raw',exist_ok=True)
json.dump(res,open(f'/home/user/1/2026-10-21-review/data/raw/{out}.json','w'),ensure_ascii=False)
s=res['series'];print(len(s),'series; sum overall =',round(sum((v['overall'] or 0) for v in s.values()),2))
