import json
R='/home/user/1/2026-10-21-review/data/raw/'
U=json.load(open(R+'derived_user_revenue_by_week.json'))
L=lambda f:{k:v['overall'] for k,v in json.load(open(R+f))['series'].items()}
fail=L('q21_failed_per_user_W41.json'); fin=L('q21_finished_per_user_W41_zc.json')
W1='7f3ad82a'
payers=[k for k in U['W41'] if k!=W1]
def bucket(k):
    n=fin.get(k,0); f=fail.get(k,0)
    if n<20: return 'a_<20 tasks / no data'
    s=f/n
    return 'b_<5%' if s<0.05 else 'c_5-10%' if s<0.10 else 'd_10-20%' if s<0.20 else 'e_>=20%'
def lvl(k):
    r=U['W41'][k]; return '1_<$300' if r<300 else '2_$300-999' if r<1000 else '3_>=$1000'
out={}
for k in payers:
    for key in [(bucket(k),'all'),(bucket(k),lvl(k))]:
        o=out.setdefault(key,[0,0,0,0]); o[0]+=1;o[1]+=U['W41'][k];o[2]+=U['W42'].get(k,0);o[3]+=(k not in U['W42'])
res=[]
for key in sorted(out):
    n,a,b,left=out[key]
    res.append({'bucket':key[0],'level':key[1],'n':n,'rev_W41':round(a),'rev_W42':round(b),'delta':round(b-a),'pct':round(100*(b/a-1),1),'left_share':round(100*left/n,1)})
    print(key,n,round(a),round(b),'%+.1f%%'%(100*(b/a-1)),'left %.0f%%'%(100*left/n))
json.dump({'note':'W41 payers excl. whale #1; failed share = failed/finished TSC in W41 (finished list truncated at 1000 users on zencreator platformType => low-volume users fall into <20 tasks bucket)','rows':res},open(R+'derived_failed_exposure_W41_vs_revenue.json','w'),ensure_ascii=False,indent=0)
