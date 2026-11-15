"""Mantel相关/偏相关及节点重抽样区间。不是Mantel置换p值检验。
默认与论文更新表4/5一致：节点次数乘积权重。可显式选择用户去重方案。
"""
from pathlib import Path
import argparse,json
import numpy as np
import pandas as pd

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--bootstrap',type=int,default=5000)
    ap.add_argument('--seed',type=int,default=42)
    ap.add_argument('--method',choices=['node_weight','endpoint_union'],default='node_weight')
    args=ap.parse_args()
    if args.bootstrap<2:ap.error('bootstrap须至少为2')
    base=Path(__file__).resolve().parent
    df=pd.read_csv(base/'data/点对数据.csv')
    names=list(dict.fromkeys(df['点1'].tolist()+df['点2'].tolist()));ids={n:i for i,n in enumerate(names)}
    # Restore original matrix order, independent of pair enumeration.
    order=pd.read_csv(base/'data/109点正确坐标.csv')['方言点'].tolist()[10:93]
    assert set(names)==set(order)
    ids={n:i for i,n in enumerate(order)};n=len(ids)
    i=df['点1'].map(ids).to_numpy();j=df['点2'].map(ids).to_numpy()
    assert len(df)==n*(n-1)//2 and np.all(i!=j)
    assert len(set(tuple(sorted(v)) for v in zip(i,j)))==len(df)
    # Distance is the corrected-coordinate Haversine km distance in the supplied table.
    cols=['历属','县界','河界','流域'];D=df['距离km'].to_numpy();assert np.all(D>0)
    z=np.column_stack([df['相似度'],df[cols],D,np.log(D)])
    assert np.isfinite(z).all()
    def calc(w):
        v=z-np.average(z,axis=0,weights=w);cov=(v*w[:,None]).T@v/w.sum();sd=np.sqrt(np.diag(cov))
        if np.any(sd==0):raise ValueError('重抽样中存在常量变量')
        c=cov/np.outer(sd,sd);r={}
        for k,label in enumerate(cols,1):
            r['原始相关/'+label]=c[0,k]
            for di,tag in [(5,'D'),(6,'lnD')]:
                r['偏相关_'+tag+'/'+label]=(c[0,k]-c[0,di]*c[k,di])/np.sqrt((1-c[0,di]**2)*(1-c[k,di]**2))
        for tag in ['D','lnD']:
            r['配对差值_'+tag+'/历史减现行']=r['偏相关_'+tag+'/历属']-r['偏相关_'+tag+'/县界']
            r['配对差值_'+tag+'/河界减流域']=r['偏相关_'+tag+'/河界']-r['偏相关_'+tag+'/流域']
        return r
    point=calc(np.ones(len(df)));rng=np.random.default_rng(args.seed);draws=[]
    for _ in range(args.bootstrap):
        counts=np.bincount(rng.integers(0,n,n),minlength=n)
        w=counts[i]*counts[j] if args.method=='node_weight' else ((counts[i]>0)|(counts[j]>0)).astype(float)
        draws.append(calc(w))
    draws=pd.DataFrame(draws);rows=[]
    for k,value in point.items():
        lo,hi=draws[k].quantile([.025,.975]);rows.append({'指标':k,'估计值':value,'SE':draws[k].std(ddof=1),'CI下限':lo,'CI上限':hi})
    out=base/('mantel_results_'+args.method);out.mkdir(exist_ok=True)
    pd.DataFrame(rows).to_csv(out/'统计结果.csv',index=False,encoding='utf-8-sig');draws.to_csv(out/'Bootstrap逐次结果.csv',index=False,encoding='utf-8-sig')
    (out/'设置.json').write_text(json.dumps(vars(args),ensure_ascii=False,indent=2),encoding='utf-8')
    print(pd.DataFrame(rows).to_string(index=False))
if __name__=='__main__':main()
