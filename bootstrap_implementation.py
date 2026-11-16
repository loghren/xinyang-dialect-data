# -*- coding: utf-8 -*-
"""
信阳方言地理分析：偏Mantel检验与中介效应的聚类Bootstrap实现（文中实现）
方法要点：
- 聚类单位 = 83个方言点；重抽单位 = 方言点
- 每次重抽后，纳入"至少一端被抽中"的全部原始点对，同一原始点对只计一次（np.unique去重）
- 不生成同一点与自身的配对；距离恒取原始球面距离，不存在距离为0、无法取对数的情形
- 点估计：OLS；显著性：按方言点聚类重抽样2000次，百分位法95%置信区间
"""
import pandas as pd
import numpy as np

# ---------- 数据 ----------
f1  = pd.read_csv('系数及是否同一区域.csv')   # 3403个点对：城市1 城市2 系数 历史 县界 河界 流域
att = pd.read_csv('分类变量及属性.csv')       # 83个点：经度 纬度 高程 坡度 等
n = len(att)                                   # 83
lon = att['经度'].values.astype(float)
lat = att['纬度'].values.astype(float)

def haversine(lo1, la1, lo2, la2):
    R = 6371.0
    p1, p2 = np.radians(la1), np.radians(la2)
    dp, dl = np.radians(la2 - la1), np.radians(lo2 - lo1)
    a = np.sin(dp/2)**2 + np.cos(p1)*np.cos(p2)*np.sin(dl/2)**2
    return 2 * R * np.arcsin(np.sqrt(a))

ii, jj = np.triu_indices(n, 1)                 # 上三角点对索引（83×82/2=3403）
dist = haversine(lon[ii], lat[ii], lon[jj], lat[jj])   # 原始球面距离，min≈3.3km
lnd  = np.log(dist)                            # 中介模型的距离控制变量

sim  = f1['系数'].values.astype(float)         # 方言相似度 Y
hj   = f1['河界'].values.astype(float)         # 河界 X
hist = f1['历史'].values.astype(float)         # 历史县界 M

# ---------- 偏Mantel（Pearson偏相关，控制距离矩阵D） ----------
def pcorr_pe(y, x, c):
    r_yx = np.corrcoef(y, x)[0, 1]
    r_yc = np.corrcoef(y, c)[0, 1]
    r_xc = np.corrcoef(x, c)[0, 1]
    return (r_yx - r_yc*r_xc) / np.sqrt((1 - r_yc**2) * (1 - r_xc**2))

# ---------- 中介模型（全线性LPM，控制lnD） ----------
def ols(yv, cols):
    X = np.column_stack([np.ones(len(yv))] + cols)
    return np.linalg.lstsq(X, yv, rcond=None)[0]

def mediation(y, x, m, d):
    c  = ols(y, [x, d])[1]                     # 总效应 c
    a  = ols(m, [x, d])[1]                     # a路径
    bb = ols(y, [x, m, d])                     # b 与 c'
    b, cp = bb[2], bb[1]
    return a, b, cp, c, a*b                    # 间接效应 a×b（恒等于 c−c′）

# ---------- 聚类Bootstrap（文中实现） ----------
# 预计算：每个方言点涉及的全部点对索引
pt_pairs = [np.where((ii == p) | (jj == p))[0] for p in range(n)]

def cluster_boot_idx(rng):
    """有放回重抽83个点，返回'至少一端被抽中'的原始点对索引（去重）"""
    samp = rng.integers(0, n, n)
    return np.unique(np.concatenate([pt_pairs[p] for p in samp]))

B = 2000
rng = np.random.default_rng(42)

boot_hj, boot_hist = [], []
boot_F = []                                       # 正向：河界→历史县界→相似度
for b in range(B):
    idx = cluster_boot_idx(rng)
    y, d = sim[idx], lnd[idx]
    x, m = hj[idx], hist[idx]
    boot_hj.append(pcorr_pe(y, x, dist[idx]))
    boot_hist.append(pcorr_pe(y, m, dist[idx]))
    boot_F.append(mediation(y, x, m, d))

boot_hj   = np.array(boot_hj)
boot_hist = np.array(boot_hist)
boot_F    = np.array(boot_F)                      # 每行 [a, b, c′, c, a×b]

# ---------- 输出 ----------
print('偏Mantel（控制距离，Pearson）')
for name, x, boot in [('河界', hj, boot_hj), ('历史县界', hist, boot_hist)]:
    est = pcorr_pe(sim, x, dist)
    se  = boot.std(ddof=1)
    lo, hi = np.percentile(boot, [2.5, 97.5])
    print(f'  {name}: r={est:.3f}  SE={se:.3f}  95%CI=[{lo:.3f}, {hi:.3f}]')

print('\n中介效应（正向链条，控制lnD，LPM）')
est = mediation(sim, hj, hist, lnd)
labels = ['a', 'b', "c′", 'c', 'a×b']
for k, lab in enumerate(labels):
    se  = boot_F[:, k].std(ddof=1)
    lo, hi = np.percentile(boot_F[:, k], [2.5, 97.5])
    print(f'  {lab}: {est[k]:+.4f}  SE={se:.4f}  95%CI=[{lo:.4f}, {hi:.4f}]')
prop = boot_F[:, 4] / boot_F[:, 3]
print(f'  间接效应占比: {est[4]/est[3]*100:.1f}%  95%CI=[{np.percentile(prop,2.5)*100:.1f}%, {np.percentile(prop,97.5)*100:.1f}%]')