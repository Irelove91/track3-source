"""Track 3 — 3D model + preview renders, from the accurate top-down layout."""
import numpy as np, trimesh, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.expanduser("~/Desktop/track3-map")
meshes=[]
def add(m,color):
    m.visual.face_colors=color; meshes.append(m)

from trimesh.creation import box, cylinder, annulus, torus
def R(deg,axis): return trimesh.transformations.rotation_matrix(np.deg2rad(deg),axis)

# palette
C_GROUND=[24,26,32,255]; C_WALL=[150,150,158,255]; C_BUSH=[57,217,138,255]
C_BRIDGE=[70,74,86,255]; C_PILLAR=[150,150,160,255]; C_RED=[255,77,77,255]
C_GRN=[57,217,138,255]; C_YEL=[255,210,63,255]; C_CYAN=[56,189,248,255]
C_ACC=[176,108,255,255]; C_H=[232,132,60,255]

# ---- ground ----
g=box(extents=[86,62,0.4]); g.apply_translation([42,30,-0.2]); add(g,C_GROUND)

# ---- wall (left) ----
w=box(extents=[0.8,40,4]); w.apply_translation([6,26,2]); add(w,C_WALL)

# ---- bushes (hedge along the top) ----
for x in np.arange(10,57,4):
    b=box(extents=[3.6,2.2,1.8]); b.apply_translation([x,48,0.9]); add(b,C_BUSH)

# ---- bridge (elevated deck you fly over / hoop hangs under) ----
deck=box(extents=[38,11,0.6])
deck.apply_transform(R(13,[0,0,1])); deck.apply_translation([42,24,3.2]); add(deck,C_BRIDGE)
for t in np.linspace(-17,17,6):                       # support columns
    px=42+t*np.cos(np.deg2rad(13)); py=24+t*np.sin(np.deg2rad(13))
    c=cylinder(radius=0.5,height=3.2,sections=10); c.apply_translation([px,py,1.6]); add(c,C_BRIDGE)

# ---- gemfan / cube gate (square tube frame) ----
def cube_gate(cx,cy,cz,s=3.0,t=0.28):
    for a,b,ext in [([0,0,s/2],0,[s,t,t]),([0,0,-s/2],0,[s,t,t]),
                    ([s/2,0,0],0,[t,t,s]),([-s/2,0,0],0,[t,t,s])]:
        e=box(extents=ext); e.apply_translation([cx+a[0],cy,cz+a[2]]); add(e,C_YEL)
cube_gate(13.2,33,2.0)          # outer pop-up gate
cube_gate(13.2,33.5,2.0,s=2.0)  # inner pop-up gate, nested just behind — matches the double-gate pair in the real footage

# ---- pillars + markers ----
def pillar(x,y,h=3.0,cap=None):
    c=cylinder(radius=0.9,height=h,sections=16); c.apply_translation([x,y,h/2]); add(c,C_PILLAR)
    if cap is not None:
        d=cylinder(radius=1.15,height=0.35,sections=20); d.apply_translation([x,y,0.2]); add(d,cap)
pillar(15,20)
pillar(14.1,7,cap=C_GRN)      # green marker
pillar(44,11,cap=C_RED)     # red marker

# ---- hoop (ring) hanging under the bridge bottom edge, above the red marker ----
ring=torus(major_radius=2.0,minor_radius=0.22,major_sections=40,minor_sections=12)
ring.apply_transform(R(90,[1,0,0]))          # stand it up (vertical, faces +y)
ring.apply_translation([44,19,2.2]); add(ring,C_CYAN)

# ---- ladder gate (4 bars = 3 equal holes: top/middle/bottom) + end legs, far right — 3.0 gap each, bottom anchored near ground ----
lx,ly=73,23.8
for dz in (9.15,6.15,3.15,0.15):
    r=box(extents=[0.3,5.7,0.3]); r.apply_translation([lx,ly,dz]); add(r,C_ACC)
for dy in (-2.85,2.85):
    p=box(extents=[0.3,0.3,9.0]); p.apply_translation([lx,ly+dy,4.65]); add(p,C_ACC)

# ---- H pad ----
disc=cylinder(radius=2.4,height=0.2,sections=40); disc.apply_translation([61,15,0.1]); add(disc,C_H)

# ---- racing line (3D tube, with altitude) ----
WP=np.array([
 (61,15,0.4),
 (53,13,0.8),(48,10.5,0.9),
 (47,13,1.0),(44,15.5,1.0),(40,13,1.0),(39.5,9,1.0),(44,7,1.0),(48,9.5,1.0),
 (47,13.5,1.1),(45,15.5,1.3),
 (46,25,3.9),(43,35,4.3),(37,43,4.4),   # step 3 climbs OVER the bridge deck (deck top ~3.5)
 (26,46,3.0),(15.9,43,2.6),
 (13.2,39,2.0),(13.2,33,1.7),
 (13.2,26,1.6),(13.2,18,1.5),(14.1,11.5,1.3),
 (14.6,9.3,1.1),(17.8,6.4,1.0),(15.2,3.2,1.0),(11.4,4.2,1.0),(10.8,7.8,1.0),(13.2,9.9,1.1),(16.8,8.6,1.1),  # 7 CW 360 — clean pigtail, no cusp
 (25,6.5,1.0),(36,9,1.0),(47,9.5,1.1),                            # 8 pass the red-marker POLE on its RIGHT (solid concrete)
 (48,14,1.4),(43,17.5,1.9),                                       #   round the pole, then LEFT toward the hoop
 (38.5,20.5,2.2),(38.5,23.5,2.4),(41.5,24.5,2.4),(44,22.5,2.4),   # step 9 STAYS UNDER the bridge deck
 (44.5,20,2.3),(44,17,1.6),                                       #   ducks under, threads the hoop from the top down
 (50,17,1.6),(62,22,3.4),(70,26,7.5),
 (71.8,26.4,7.65),(72.2,27.6,7.65),(73.4,27.8,7.65),(74.2,26.9,7.65),(73.8,25.7,7.65),(72.6,25.5,7.65),  # 10a tight 360 through the TOP hole
 (71.8,26.4,4.65),(72.2,27.6,4.65),(73.4,27.8,4.65),(74.2,26.9,4.65),(73.8,25.7,4.65),(72.6,25.5,4.65),  # 10b tight 360 through the MIDDLE hole — identical radius/shape to 10a
 (72.0,25.9,1.65),(70.2,25.9,0.5),   # 10c BOTTOM hole — straight out, no loop
 (69,21,0.5),
 (66,17,0.8),(61,15,0.4),
])
def cr(P,n=16):
    ext=np.vstack([P[0],P,P[-1]]);o=[]
    for i in range(1,len(ext)-2):
        p0,p1,p2,p3=ext[i-1],ext[i],ext[i+1],ext[i+2]
        for j in range(n):
            s=j/n;s2=s*s;s3=s2*s
            o.append(0.5*((2*p1)+(-p0+p2)*s+(2*p0-5*p1+4*p2-p3)*s2+(-p0+3*p1-3*p2+p3)*s3))
    o.append(P[-1]);return np.array(o)
line=cr(WP)
segs=[]
for i in range(len(line)-1):
    segs.append(cylinder(radius=0.16,segment=[line[i],line[i+1]],sections=8))
tube=trimesh.util.concatenate(segs); add(tube,C_ACC)

# ---- numbered step markers (match the 2D map) ----
BADGES=[(1,64,17,0.9),(2,44,11,1.6),(3,49,24,3.6),(4,22,44,2.9),(5,16.8,35,1.8),
        (6,18.6,20,1.7),(7,14.1,7,1.6),(8,37.5,14,1.6),(9,35,24,2.6),(10,76,26.8,9.55)]
for n,x,y,z in BADGES:
    s=trimesh.creation.icosphere(subdivisions=2,radius=0.95); s.apply_translation([x,y,z])
    add(s, C_RED if n==5 else (C_GRN if n==9 else C_ACC))   # 5 red, 9 green

# ---- export ----
scene=trimesh.Scene(meshes)
scene.export(f"{OUT}/track3.glb")
scene.export(f"{OUT}/track3.obj")
print("exported track3.glb / track3.obj  ·  parts:",len(meshes))

# ---- preview renders (custom depth-sorted projection) ----
from matplotlib.collections import PolyCollection
def render(fname,elev,azim,zex=1.7):
    a=np.deg2rad(azim); e=np.deg2rad(elev)
    Rz=np.array([[np.cos(a),-np.sin(a),0],[np.sin(a),np.cos(a),0],[0,0,1]])
    Rx=np.array([[1,0,0],[0,np.cos(e),-np.sin(e)],[0,np.sin(e),np.cos(e)]])
    M=Rx@Rz
    light=np.array([0.4,-0.6,0.9]); light/=np.linalg.norm(light)
    polys=[]
    for m in meshes:
        V=m.vertices.copy(); V[:,2]*=zex; Q=V@M.T
        col=np.array(m.visual.face_colors[0][:3])/255
        for f in m.faces:
            tri=V[f]; n=np.cross(tri[1]-tri[0],tri[2]-tri[0]); nl=np.linalg.norm(n)
            if nl<1e-9: continue
            shade=0.5+0.5*max(0,abs((n/nl)@light))
            polys.append((Q[f,1].mean(),Q[f][:,[0,2]],np.clip(col*shade,0,1)))
    polys.sort(key=lambda t:-t[0])
    fig,ax=plt.subplots(figsize=(11,8)); fig.patch.set_facecolor("#0e0f13"); ax.set_facecolor("#0e0f13")
    ax.add_collection(PolyCollection([p[1] for p in polys],
                     facecolors=[p[2] for p in polys],edgecolors="none",antialiased=True))
    L=line.copy(); L[:,2]*=zex; QL=L@M.T
    ax.plot(QL[:,0],QL[:,2],color="#e6ccff",lw=2.6,zorder=1e6,solid_capstyle="round")
    for n,x,y,z in BADGES:
        q=np.array([x,y,z*zex])@M.T
        ax.text(q[0],q[2],str(n),color=("#08281a" if n==9 else "#fff"),fontsize=10,ha="center",va="center",
                weight="bold",zorder=2e6,
                bbox=dict(boxstyle="circle,pad=0.22",
                          fc=("#ff4d4d" if n==5 else ("#39d98a" if n==9 else "#b06cff")),ec="white",lw=1.2))
    q=np.array([35,24,2.6*zex])@M.T
    ax.text(q[0]-2,q[2],"under bridge",color="#b06cff",fontsize=9,ha="center",
            va="center",weight="bold",rotation=90,zorder=2e6)
    ax.autoscale(); ax.set_aspect("equal"); ax.axis("off")
    plt.savefig(f"{OUT}/{fname}",dpi=120,facecolor="#0e0f13",bbox_inches="tight")
    plt.close(); print("rendered",fname)
render("track3-3d-iso.png",28,-58)
render("track3-3d-front.png",10,-90)
render("track3-3d-top.png",82,-90)
