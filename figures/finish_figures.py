from pathlib import Path
import importlib.util,json,inspect
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pyproj import Transformer,Geod

OUT=Path(__file__).resolve().parent
ROOT=Path(r'G:\Codex\Jiangsu_HumanBird_Tradeoff\03_数据库\投稿前重构_20260904\Reanalysis_v2')
spec=importlib.util.spec_from_file_location('map_source',ROOT/'figures_v2/gen_fig1_nature_rebuild.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
src=inspect.getsource(m.geometry_panel).replace('native 30 m grid','30 m product grid').replace('No reprojection · exact area weights','No raster resampling · fractional overlap')
exec(src,m.__dict__)
parks,zones,province,cities,china,comp,audit=m.load_data()
blank=parks.City_Name.eq('')|parks.City_Name.isna()
assert parks.loc[blank,'Park_ID'].tolist()==['LYG_0008']
assert parks.loc[parks.Park_ID.str.startswith('LYG_')&~blank,'City_Name'].eq('连云港市').all()
parks.loc[blank,'City_Name']='连云港市'  # Figure-only ID-prefix assignment, not model-data repair.
minx,miny,maxx,maxy=province.total_bounds
x=minx+(maxx-minx)*.05;y=miny+(maxy-miny)*.065
tr=Transformer.from_crs(parks.crs,4326,always_xy=True);geod=Geod(ellps='WGS84')
a,b=tr.transform(x,y)
lo,hi=90000.,110000.
for _ in range(50):
    mid=(lo+hi)/2;c,d=tr.transform(x+mid,y)
    if geod.inv(a,b,c,d)[2]<100000:lo=mid
    else:hi=mid
m.scale_length=(lo+hi)/2
exec(inspect.getsource(m.draw_scalebar).replace('seg = km * 1000 / 2','seg = scale_length / 2').replace('2.15 * seg','2.6 * seg'),m.__dict__)
# The original polygon-within join can omit parks crossing a city boundary.
# Classify representative points for map counts, then verify one city per park.
import geopandas as gpd
points=parks.copy();points.geometry=parks.representative_point()
joined=gpd.sjoin(points[['Park_ID','geometry']],cities[['NAME_2','geometry']],how='left',predicate='within')
print('Spatial-join diagnostic',len(joined),int(joined.index_right.isna().sum()),cities.NAME_2.tolist(),flush=True)
names={'南京市':'Nanjing','苏州市':'Suzhou','无锡市':'Wuxi','常州市':'Changzhou','淮安市':"Huai'an",'宿迁市':'Suqian','连云港市':'Lianyungang','镇江市':'Zhenjiang','盐城市':'Yancheng','扬州市':'Yangzhou','泰州市':'Taizhou','南通市':'Nantong','徐州市':'Xuzhou'}
counts=parks.City_Name.map(names).value_counts()
assert counts.sum()==1034 and len(counts)==13
# Match known inventory city names to this boundary source, normalizing punctuation.
norm=lambda s: ''.join(c for c in s.lower() if c.isalpha()).removesuffix('shi')
lookup={norm(n):i for i,n in cities.NAME_2.items()}
assert all(norm(n) in lookup for n in counts.index)
counts.rename('inventoried_parks').to_csv(OUT/'figures/Fig1_city_counts.csv')
source=inspect.getsource(m.draw_study_system)
start=source.index('    joined = ');end=source.index('    points = cities.representative_point()')
source=source[:start]+"    counts = parks.City_Name.map(city_indices).value_counts()\n"+source[end:]
m.city_indices={cn:lookup[norm(en)] for cn,en in names.items()}
exec(source,m.__dict__)

def flow(ax):
    m.clean(ax);ax.set_xlim(0,1);ax.set_ylim(0,1)
    blocks=[(.88,'Eight mapped classes','Replace zeros, then combine shrub + grass\nand water + herbaceous wetland'),
            (.65,'Six parts and five ILR balances','B1 built + bare / other covers\nB2 tree + low vegetation / crop + wet\nB3 tree / low vegetation\nB4 crop / wet cover    B5 built / bare'),
            (.38,'Two park-level responses','Median paired interior LST\nMedian same-scene ring − interior difference\nControls: log area, annual NTL and city'),
            (.13,'Specified donor–recipient transfers','Recalculate all five ILR coordinates\nReport projected change, donor count\nand pointwise city-block bootstrap interval')]
    for y,title,body in blocks:
        ax.text(.02,y,title,fontsize=7,fontweight='bold',va='top',color='#222222')
        ax.text(.02,y-.055,body,fontsize=6,va='top',linespacing=1.5,color='#404040')
    for y in [.70,.43,.18]: ax.annotate('',xy=(.47,y-.025),xytext=(.47,y+.025),arrowprops=dict(arrowstyle='->',color='#777777',lw=.6))

fig=plt.figure(figsize=(183/25.4,120/25.4))
gs=fig.add_gridspec(1,3,width_ratios=[1.05,1,1.22],left=.03,right=.99,bottom=.04,top=.92,wspace=.20)
axs=[fig.add_subplot(gs[0,i]) for i in range(3)]
for ax,label,title in zip(axs,'abc',['Study system','Geometry and extraction','Composition and prediction']):
    pos=ax.get_position();fig.text(pos.x0,.96,label,weight='bold',fontsize=9)
    fig.text(pos.x0+.025,.96,title,fontsize=7)
m.draw_study_system(axs[0],points,province,cities,china)
# Remove legacy map annotations which overlap symbols at this aspect ratio.
for t in list(axs[0].texts):
    if 'inventoried parks' in t.get_text() or 'China Albers' in t.get_text():t.remove()
fig.text(.03,.89,'1,034 inventoried parks\n728 complete-case parks\n13 Jiangsu cities',fontsize=6,va='top',linespacing=1.5)
fig.text(.03,.23,'China Albers equal-area\nSymbol area = parks per city',fontsize=5.5,va='top',linespacing=1.4)
m.geometry_panel(axs[1],parks,zones,audit);flow(axs[2])
fig.savefig(OUT/'figures/Fig1_study_design.svg',format='svg')
fig.savefig(OUT/'figures/Fig1_study_design.pdf',format='pdf')
fig.savefig(OUT/'figures/Fig1_study_design.png',dpi=600)
plt.close(fig)
# Evaluate the actual horizontal 100 km scale-bar location geodesically.
minx,miny,maxx,maxy=province.total_bounds
x=minx+(maxx-minx)*.05;y=miny+(maxy-miny)*.065
tr=Transformer.from_crs(parks.crs,4326,always_xy=True)
a,b=tr.transform(x,y);c,d=tr.transform(x+m.scale_length,y)
_,_,dist=Geod(ellps='WGS84').inv(a,b,c,d)
(OUT/'FIG1_AUDIT.json').write_text(json.dumps({'crs':str(parks.crs),'map_symbols':'area proportional to inventoried park count per city; not individual park area','park_count':int(counts.sum()),'city_count':len(counts),'scale_bar_projected_m':100000,'scale_bar_geodesic_m':dist,'scale_bar_relative_error':100000/dist-1,'ring_panel':'normalized illustration, not a scale drawing','unmatched_representative_points':int(joined.index_right.isna().sum()),'corrections':['native thermal grid label','model controls','median aggregation','incorrect SBP tree removed','donor availability terminology','city counts use original inventory City_Name; administrative boundary geometry only positions symbols']},indent=2),encoding='utf-8')
print('Figure 1 verified and redrawn',dist)
auditpath=OUT/'FIG1_AUDIT.json';qa=json.loads(auditpath.read_text())
qa['scale_bar_projected_m']=m.scale_length
qa['figure_only_city_assignment']={'Park_ID':'LYG_0008','blank_City_Name_assigned':'Lianyungang','basis':'LYG prefix verified against other named records; no model-data changes'}
auditpath.write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
