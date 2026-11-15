"""普通克里金插值：当前109点、中心保持归一化、球状变异函数及逐折重拟合留一验证。"""
import sys,os,json
from pathlib import Path
BASE=Path(__file__).resolve().parent
import numpy as np,pandas as pd,shapefile
from pyproj import Transformer
from pykrige.ok import OrdinaryKriging
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
out=BASE/'kriging_results';out.mkdir(exist_ok=True)
s=pd.read_excel(BASE/'data/相似度矩阵.xls',index_col=0)
assert list(s.index)==list(s.columns)
a=s.to_numpy(float);assert a.shape==(109,109) and np.allclose(a,a.T) and np.allclose(a.diagonal(),1)
p=pd.read_csv(BASE/'data/109点正确坐标.csv')
p=p.set_index('方言点').loc[s.index].reset_index()
lon=p['经度'].to_numpy(float);lat=p['纬度'].to_numpy(float)
h=list(range(10));z=list(range(99,109))
H=np.array([a[i,[j for j in h if j!=i]].mean() for i in range(109)])
Z=np.array([a[i,[j for j in z if j!=i]].mean() for i in range(109)])
r=H/(H+Z);L=float(np.max(abs(r-.5)))
if L==0: raise ValueError('所有系数均为0.5，无可绘制的分界线')
q=.5+(r-.5)/(2*L)
assert np.array_equal(r>.5,q>.5)
old=(r-r.min())/(r.max()-r.min())
df=pd.DataFrame({'方言点':s.index,'经度':lon,'纬度':lat,'黄孝平均相似度':H,'中原平均相似度':Z,'原始接近系数':r,'旧极差归一化':old,'中心保持归一化':q,'市内83点':[10<=i<93 for i in range(109)]})
df.to_csv(out/'109点接近系数.csv',index=False,encoding='utf-8-sig')
print('range',r.min(),r.max(),'L',L,'q',q.min(),q.max(),flush=True)
print(df[df['方言点']=='罗山'].to_string(index=False),flush=True)
tr=Transformer.from_crs('EPSG:4326','EPSG:32650',always_xy=True)
x,y=tr.transform(lon,lat);x=np.asarray(x)/1000;y=np.asarray(y)/1000
# Ordinary kriging, full neighborhood, spherical variogram fitted to 12 lag bins.
ok=OrdinaryKriging(x,y,q,variogram_model='spherical',nlags=12,weight=True,exact_values=True,verbose=False)
root=str(BASE/'data')+os.sep
rd=shapefile.Reader(root+'现行县界.shp',encoding='utf-8')
lines=[]
for sh in rd.shapes():
 pts=np.asarray(sh.points);xx,yy=tr.transform(pts[:,0],pts[:,1]);xy=np.column_stack([np.array(xx)/1000,np.array(yy)/1000]);parts=list(sh.parts)+[len(pts)]
 for i,j in zip(parts[:-1],parts[1:]):lines.append(xy[i:j])
allxy=np.vstack(lines);xmin,ymin=allxy.min(axis=0)-[12,10];xmax,ymax=allxy.max(axis=0)+[12,7]
gx=np.arange(xmin,xmax+.5,.5);gy=np.arange(ymin,ymax+.5,.5)
field,var=ok.execute('grid',gx,gy,backend='vectorized')
pred,_=ok.execute('points',x,y);assert np.max(abs(pred-q))<1e-6
# Explicit leave-one-out validation with variogram refit in every fold.
cv=[]
for i in range(109):
 keep=np.arange(109)!=i
 ko=OrdinaryKriging(x[keep],y[keep],q[keep],variogram_model='spherical',nlags=12,weight=True,exact_values=True)
 v,_=ko.execute('points',x[i:i+1],y[i:i+1]);cv.append(float(v[0]))
df['留一预测']=cv;df['留一残差']=np.array(cv)-q;df.to_csv(out/'109点接近系数.csv',index=False,encoding='utf-8-sig')
cn=FontProperties(fname=str(BASE/'data/SimSun.ttf'));en=FontProperties(family='DejaVu Serif')
from matplotlib.colors import LinearSegmentedColormap
ref_cmap=LinearSegmentedColormap.from_list('reference',[(0,'#6400ff'),(.13,'#626bff'),(.27,'#4fb5ff'),(.35,'#00e8f3'),(.48,'#8effc3'),(.60,'#caff7b'),(.69,'#ffff00'),(.82,'#ffb600'),(1,'#ff2519')],N=512)
plt.rcParams.update({'svg.fonttype':'path','pdf.fonttype':42})
fig,ax=plt.subplots(figsize=(12,7.4));fig.subplots_adjust(left=.025,right=.88,bottom=.045,top=.98)
im=ax.pcolormesh(gx,gy,field,cmap=ref_cmap,vmin=0,vmax=1,shading='auto',rasterized=True)
for line in lines:ax.plot(line[:,0],line[:,1],color='#242424',lw=.85)
cs=ax.contour(gx,gy,field,levels=[.5],colors=['#8c1515'],linewidths=2.6)
ax.clabel(cs,fmt='0.5',fontsize=13,inline=True)
ax.scatter(x[10:93],y[10:93],s=13,c='black',zorder=5)
for name,label,offset in [('信阳','浉河区',(-11,-5)),('罗山','罗山县',(0,-5)),('光山','光山县',(0,-5)),('新县','新县',(0,-5)),('息县','息县',(0,4)),('潢川','潢川县',(0,4)),('固始','固始县',(0,-5)),('商城','商城县',(0,-5)),('淮滨','淮滨县',(0,4))]:
 i=list(s.index).index(name);ax.scatter(x[i],y[i],s=78,c='white',edgecolors='#444444',linewidths=1.2,zorder=6);ax.scatter(x[i],y[i],s=12,c='#333333',zorder=7)
 ax.text(x[i]+offset[0],y[i]+offset[1],label,fontproperties=cn,fontsize=12,ha='center',va='center',color='#303030',zorder=8)
ax.set(xlim=(xmin,xmax),ylim=(ymin,ymax),aspect='equal');ax.axis('off')
cax=fig.add_axes([.91,.10,.025,.80]);cb=fig.colorbar(im,cax=cax,ticks=[0,.5,1]);cb.outline.set_visible(False)
for t in cb.ax.get_yticklabels():t.set_fontproperties(en);t.set_fontsize(13)
fig.savefig(out/'黄孝接近系数_克里金插值.png',dpi=350,facecolor='white')
fig.savefig(out/'黄孝接近系数_克里金插值.svg',facecolor='white')
plt.close(fig)
features=[]
inv=Transformer.from_crs('EPSG:32650','EPSG:4326',always_xy=True)
for seg in cs.allsegs[0]:
 if len(seg)>1:
  lo,la=inv.transform(seg[:,0]*1000,seg[:,1]*1000);features.append({'type':'Feature','properties':{'level':.5},'geometry':{'type':'LineString','coordinates':np.column_stack([lo,la]).tolist()}})
(out/'0.5等值线.geojson').write_text(json.dumps({'type':'FeatureCollection','features':features},ensure_ascii=False))
np.savez_compressed(out/'插值网格.npz',x_km=gx,y_km=gy,value=np.asarray(field),variance=np.asarray(var),crs='EPSG:32650')
info={'r_min':float(r.min()),'r_max':float(r.max()),'L':L,'variogram_parameters_psill_range_nugget':ok.variogram_model_parameters.tolist(),'LOOCV_RMSE':float(np.sqrt(np.mean((np.array(cv)-q)**2))),'LOOCV_MAE':float(np.mean(abs(np.array(cv)-q))),'grid_range':[float(field.min()),float(field.max())],'classification_changes':int(np.sum((r>.5)!=(q>.5)))}
(out/'参数记录.json').write_text(json.dumps(info,ensure_ascii=False,indent=2));print(info,flush=True)