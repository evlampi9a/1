import json
R='/home/user/1/2026-10-21-review/data/raw/'
W1='7f3ad82a-4262-49a6-b592-9287e8ae69bf'
def load(p,w): return {k:v['overall'] for k,v in json.load(open(f'{R}q02_{p}_users_{w}.json'))['series'].items() if v['overall']}
U={}
for w in ['W40','W41','W42']:
    om,zc=load('openmov',w),load('zencreator',w)
    U[w]={}
    for d in (om,zc):
        for k,v in d.items(): U[w][k]=U[w].get(k,0)+v
    w1=om.get(W1,0)+zc.get(W1,0)
    print(w,'total',round(sum(U[w].values()),2),'#1',w1,'om ex#1',round(sum(om.values())-om.get(W1,0),2),'zc',round(sum(zc.values()),2),'zc payers',len(zc),'zc/payer',round(sum(zc.values())/len(zc),1),'om payers',len(om),'om ex1',len(om)-(W1 in om),'all payers',len(U[w]),'both-plat',len(set(om)&set(zc)))
def churn(a,b):
    A,B=U[a],U[b];L=set(A)-set(B);C=set(B)-set(A);Bo=set(A)&set(B)
    print(f'{a}->{b}: left n={len(L)} rev {round(sum(A[k] for k in L))}; came n={len(C)} rev {round(sum(B[k] for k in C))}; both n={len(Bo)} {round(sum(A[k] for k in Bo))}->{round(sum(B[k] for k in Bo))} d={round(sum(B[k]-A[k] for k in Bo))}')
    print(' check delta', round(sum(B.values())-sum(A.values())), '=', round(-sum(A[k] for k in L)+sum(B[k] for k in C)+sum(B[k]-A[k] for k in Bo)))
    dr=sorted(Bo,key=lambda k:B[k]-A[k])
    print(' top10 drops',[(k[:8],round(A[k]),round(B[k])) for k in dr[:10]],'sum',round(sum(B[k]-A[k] for k in dr[:10])))
    print(' top5 gains',[(k[:8],round(A[k]),round(B[k])) for k in dr[-5:]])
    print(' top left',sorted([(round(A[k]),k[:8]) for k in L],reverse=True)[:8])
    print(' top came',sorted([(round(B[k]),k[:8]) for k in C],reverse=True)[:8])
    return L,C,Bo
churn('W40','W41'); r=churn('W41','W42')
json.dump({w:U[w] for w in U},open(R+'derived_user_revenue_by_week.json','w'))
