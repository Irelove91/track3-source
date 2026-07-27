"""Track 3 — top-down map (IMG_5961 route, IMG_5963 bushes/bridge update)."""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon

BG="#0e0f13"; INK="#e8e8ec"; MUT="#9aa0aa"; ACC="#b06cff"
RED="#ff4d4d"; GRN="#39d98a"; YEL="#ffd23f"; CYAN="#38bdf8"

fig,ax=plt.subplots(figsize=(13,9)); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
def T(x,y,s,c=INK,sz=12,rot=0,ha="center",wt="bold"):
    ax.text(x,y,s,color=c,fontsize=sz,rotation=rot,ha=ha,va="center",weight=wt,zorder=7)

# ---- wall (left) + bushes (flat horizontal line across the top) ----
ax.plot([6,6],[6,46],color=MUT,lw=4,zorder=2); T(3.4,26,"WALL",MUT,12,90)
ax.plot([10,56],[48,48],color=GRN,lw=4,zorder=2)
for x in np.arange(12,55,5): ax.plot([x-1,x+1],[46.4,47.4],color=GRN,lw=2.2,alpha=.8,zorder=2)
T(33,50.5,"BUSHES",GRN,12)

# ---- bridge (wider; bottom edge kept near the hoop/red marker) ----
c=np.array([42,24]); ang=np.deg2rad(13); L,Wd=38,11
d=np.array([np.cos(ang),np.sin(ang)]); p=np.array([-d[1],d[0]])
corn=[c-L/2*d-Wd/2*p, c-L/2*d+Wd/2*p, c+L/2*d+Wd/2*p, c+L/2*d-Wd/2*p]
ax.add_patch(Polygon(corn,closed=True,facecolor="#2a2d36",edgecolor="#3a3f4a",lw=1.2,zorder=1))
T(56,28,"BRIDGE",MUT,12,13)
T(50,28,"over bridge",ACC,10,rot=-62)

# ---- gemfan / cube gate (left) ----
ax.add_patch(Rectangle((10.5,30.3),5.4,5.4,fill=False,edgecolor=YEL,lw=2.5,zorder=4))
ax.add_patch(Rectangle((11.4,31.2),3.6,3.6,fill=False,edgecolor=YEL,lw=1.2,zorder=4))
T(13.2,37.8,"GEMFAN / CUBE GATE",YEL,10)

# ---- pillars ----
def pillar(x,y,name,dy=-3.0):
    ax.add_patch(Circle((x,y),1.6,facecolor="#3a3f4a",edgecolor=INK,lw=1.4,zorder=3))
    if name: T(x,y+dy,name,MUT,10,wt="normal")
pillar(15,20,"pillar")
# green-marker pillar (step 7) — same format as the red marker
GP=(14.1,7)
ax.add_patch(Circle(GP,1.95,facecolor="#3a3f4a",edgecolor=INK,lw=1.2,zorder=3))
ax.add_patch(Circle(GP,1.5,facecolor=GRN,edgecolor="#fff",lw=1.4,zorder=6))
T(GP[0],GP[1],"7","#08281a",12,wt="bold")   # number 7 sits inside the green marker
T(19,7,"green marker (7)",GRN,10,ha="left",wt="normal")
T(19,4.6,"(360° right)",MUT,9,ha="left",wt="normal")

# ---- red-marker pillar (steps 2 AND 8) ----
RP=(44,11)
ax.add_patch(Circle(RP,1.95,facecolor="#3a3f4a",edgecolor=INK,lw=1.2,zorder=3))
ax.add_patch(Circle(RP,1.5,facecolor=RED,edgecolor="#fff",lw=1.4,zorder=6))
T(RP[0],RP[1],"2","#fff",12,wt="bold")   # number 2 sits inside the red marker
T(RP[0]+3.6,RP[1],"red marker (2 & 8)",RED,10,ha="left",wt="normal")
T(RP[0]+3.6,RP[1]-2.4,"(360° then left)",MUT,9,ha="left",wt="normal")

# ---- hoop gate: on the bottom edge of the bridge, directly above the red marker ----
HP=(44,19)
ax.add_patch(Circle(HP,2.2,fill=False,edgecolor=CYAN,lw=3,zorder=4)); T(48,19.5,"HOOP",CYAN,10,ha="left")

# ---- ladder gate (4 rungs = 3 equal holes: top/middle/bottom), far right — upright like a real ladder: 2 full legs + 4 horizontal rungs ----
lx,ly=73,23.8
for dy in (4.5,1.5,-1.5,-4.5): ax.plot([lx-2.7,lx+2.7],[ly+dy,ly+dy],color=ACC,lw=2.2,zorder=6)
ax.plot([lx-2.7,lx-2.7],[ly-4.5,ly+4.5],color=ACC,lw=2.6,zorder=6)
ax.plot([lx+2.7,lx+2.7],[ly-4.5,ly+4.5],color=ACC,lw=2.6,zorder=6)
for i,s in enumerate(("top","middle","bottom")): T(lx+3.4,ly+3.0-i*3.0,s,ACC,9,ha="left",wt="normal")
T(lx,ly-6,"LADDER GATE",ACC,10)

# ---- H start/finish (brought down; H->2 runs parallel to the bridge) ----
ax.add_patch(Circle((61,15),2.4,facecolor="#e8843c",edgecolor="#fff",lw=1.5,zorder=6))
T(61,15,"H","#1a1a1a",15); T(61,11,"START / FINISH",INK,10)
pillar(67,12,"pillar")   # between the bridge and the ladder gate, right of the START/FINISH text

# ---- racing line ----
WP=np.array([
 (61,15),                                                    # 1 H start (brought down)
 (53,13),(48,10.5),                                          # STRAIGHT from H, passing the marker slightly on the right
 (45.8,12.2),(44,13.7),(41.6,12.2),(41.3,9.8),(44,8.6),(46.4,10.1),  # 2 full 360 CCW — TIGHT coil around the marker (distinct from the other passes)
 (45.8,12.4),(44.6,13.7),                                    #   close, then continue up-left
 (46,25),(43,35),(37,43),                                    # 3 over the bridge — curving naturally toward marker 4
 (26,46),(15.9,43),                                          # 4 top-left, then down toward gemfan
 (13.2,39),(13.2,33),                                        # 5 gemfan / cube gate (LEFT)
 (13.2,26),(13.2,18),(14.1,11.5),                            # 6 STRAIGHT down past pillar 6
 (14.6,9.3),(17.8,6.4),(15.2,3.2),(11.4,4.2),(10.8,7.8),(13.2,9.9),(16.8,8.6),  # 7 full 360 RIGHT — clean pigtail crossing, no cusp
 (25,6.5),(36,9),(49,9.5),                                   # 8 come back, pass the red-marker POLE on its RIGHT (solid) — nudged right to clear coil 2
 (49.5,14),(43,17.5),                                        #   round the pole, then LEFT toward the hoop
 (38.5,20.5),(38.5,23.5),(41.5,24.5),(44,22.5),              # 9 TIGHT loop to the left, over the top
 (44.5,20),(44,17),                                          #   through the hoop TOP -> DOWN (tight)
 (50,17),(62,22),(70,26),                                    #   then across to the ladder
 (71.7,26.6),(72.2,27.8),(73.5,28.0),(74.3,27.0),(73.8,25.8),(72.6,25.6),   # 10a top hole — circle, matches 3D
 (71.7,23.6),(72.2,24.8),(73.5,25.0),(74.3,24.0),(73.8,22.8),(72.6,22.6),   # 10b middle hole — circle, matches 3D
 (71.7,20.6),(72.2,21.8),(73.5,22.0),(74.3,21.0),(73.8,19.8),(72.6,19.6),   # 10c bottom hole — circle, matches 3D
 (71.3,19.4),(70.0,19.2),                                                  #   then straight out on the exit tangent, matches 3D
 (66,17),(61,15),                                            #   out, through H = finish
])
def cr(P,n=22):
    ext=np.vstack([P[0],P,P[-1]]);o=[]
    for i in range(1,len(ext)-2):
        p0,p1,p2,p3=ext[i-1],ext[i],ext[i+1],ext[i+2]
        for j in range(n):
            s=j/n;s2=s*s;s3=s2*s
            o.append(0.5*((2*p1)+(-p0+p2)*s+(2*p0-5*p1+4*p2-p3)*s2+(-p0+3*p1-3*p2+p3)*s3))
    o.append(P[-1]);return np.array(o)
sm=cr(WP)
ax.plot(sm[:,0],sm[:,1],color=ACC,lw=3.2,alpha=.95,zorder=5,solid_capstyle="round")
for i in range(10,len(sm)-14,40):
    d2=sm[i+5]-sm[i]; nn=np.hypot(*d2) or 1; d2=d2/nn
    ax.annotate("",xy=(sm[i]+d2*0.4),xytext=sm[i],
        arrowprops=dict(arrowstyle="-|>",color="#d9b8ff",lw=0,mutation_scale=15),zorder=6)

# ---- step badges ----
B=[(1,64,17),(3,49,24),(4,22,44),(6,18.6,20),
   (8,49,5.5),(9,35,24),(10,74.5,29.5)]
for n,bx2,by2 in B:
    fc = GRN if n==9 else ACC
    tc = "#08281a" if n==9 else "#fff"      # marker 9 is green
    ax.add_patch(Circle((bx2,by2),1.55,facecolor=fc,edgecolor="#fff",lw=1,zorder=8))
    ax.text(bx2,by2,str(n),color=tc,fontsize=10,ha="center",va="center",weight="bold",zorder=9)

# marker 5 — a red mark, same style as marker 2
ax.add_patch(Circle((16.8,35),1.95,facecolor="#3a3f4a",edgecolor=INK,lw=1.2,zorder=8))
ax.add_patch(Circle((16.8,35),1.5,facecolor=RED,edgecolor="#fff",lw=1.4,zorder=8))
ax.text(16.8,35,"5",color="#fff",fontsize=12,ha="center",va="center",weight="bold",zorder=9)

T(30,24,"under bridge",ACC,9,90)   # vertical, like the WALL label

T(6,58,"TRACK 3",INK,26,ha="left")
ax.text(6,55.4,"top-down · your numbered route + bushes/bridge update · lap 1",color=MUT,fontsize=12,ha="left")
ax.text(64,54,"Lap 1: ladder CW, top → bottom.\nLap 2: ladder CCW, bottom → top.\nFinish: back through the H.",
        color=INK,fontsize=11,va="top",ha="left",
        bbox=dict(boxstyle="round,pad=0.6",fc="#1a1c22",ec=ACC,lw=1.2))

ax.set_xlim(0,84); ax.set_ylim(0,60); ax.set_aspect("equal"); ax.axis("off")
plt.tight_layout()
plt.savefig("/Users/djgato/Desktop/track3-map/track3-plan.png",dpi=130,facecolor=BG,bbox_inches="tight")
print("saved")
