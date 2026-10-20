import json
R='/home/user/1/2026-10-21-review/data/raw/'
def load(p,w): return {k:v['overall'] for k,v in json.load(open(f'{R}q02_{p}_users_{w}.json'))['series'].items() if v['overall']}
out={}
for p in ['zencreator','openmov']:
    A,B=load(p,'W41'),load(p,'W42')
    L=set(A)-set(B);C=set(B)-set(A);Bo=set(A)&set(B)
    r={'left_n':len(L),'left_rev_W41':round(sum(A[k] for k in L)),'came_n':len(C),'came_rev_W42':round(sum(B[k] for k in C)),'both_n':len(Bo),'both_W41':round(sum(A[k] for k in Bo)),'both_W42':round(sum(B[k] for k in Bo))}
    r['both_delta']=r['both_W42']-r['both_W41'];r['net']=r['came_rev_W42']-r['left_rev_W41']+r['both_delta']
    # inc/dec among both
    r['both_up_n']=sum(1 for k in Bo if B[k]>A[k]);r['both_down_n']=sum(1 for k in Bo if B[k]<A[k])
    out[p]=r;print(p,r)
U=json.load(open(R+'derived_user_revenue_by_week.json'))
A,B=U['W41'],U['W42'];Bo=set(A)&set(B)
dr=sorted(Bo,key=lambda k:B[k]-A[k])
out['top10_drops_paid_both']=[{'user':k[:8],'W41':round(A[k]),'W42':round(B[k]),'delta':round(B[k]-A[k])} for k in dr[:10]]
out['top5_gains_paid_both']=[{'user':k[:8],'W41':round(A[k]),'W42':round(B[k]),'delta':round(B[k]-A[k])} for k in dr[::-1][:5]]
out['top_left']=[{'user':k[:8],'W41':round(A[k])} for k in sorted(set(A)-set(B),key=lambda k:-A[k])[:5]]
out['top_came']=[{'user':k[:8],'W42':round(B[k])} for k in sorted(set(B)-set(A),key=lambda k:-B[k])[:5]]
both_down=sum(B[k]-A[k] for k in Bo if B[k]<A[k]);both_up=sum(B[k]-A[k] for k in Bo if B[k]>A[k])
out['both_down_sum']=round(both_down);out['both_up_sum']=round(both_up)
print('both down',round(both_down),'up',round(both_up))
json.dump(out,open(R+'derived_churn_W41_W42.json','w'),ensure_ascii=False,indent=1)
# platform for top drops
zc41,zc42,om41,om42=load('zencreator','W41'),load('zencreator','W42'),load('openmov','W41'),load('openmov','W42')
for k in dr[:10]: print(k[:8],'zc',round(zc41.get(k,0)),round(zc42.get(k,0)),'om',round(om41.get(k,0)),round(om42.get(k,0)))
