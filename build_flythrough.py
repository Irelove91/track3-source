"""Track 3 — chase-cam fly-through of the racing line through the 3D course."""
import build_3d as B                      # builds meshes + line (reuses the exact geometry)
import numpy as np, os, subprocess
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection

OUT=B.OUT; line=B.line
env=[m for m in B.meshes if m is not B.tube and len(m.vertices)!=162]  # drop tube + badge spheres
env=[m for m in env if not (list(np.asarray(m.visual.face_colors[0][:3]))==[70,74,86] and len(m.vertices)!=8)]  # drop bridge SUPPORT LEGS (keep the deck box) — they read as random pillars in the fly-through

# gather triangles
tri=[]; col=[]
for m in env:
    c=np.array(m.visual.face_colors[0][:3])/255.
    F=m.faces; tri.append(m.vertices[F]); col.append(np.tile(c,(len(F),1)))
tri=np.concatenate(tri); col=np.concatenate(col)          # (N,3,3),(N,3)
e1=tri[:,1]-tri[:,0]; e2=tri[:,2]-tri[:,0]
nrm=np.cross(e1,e2); nrm/=np.clip(np.linalg.norm(nrm,axis=1,keepdims=True),1e-9,None)
CYAN=np.array([56,189,248])/255.; cyanmask=np.all(np.abs(col-CYAN)<0.06,axis=1)  # the hoop ring faces

WUP=np.array([0,0,1.]); light=np.array([0.4,-0.6,0.9]); light/=np.linalg.norm(light)
def nz(v): return v/(np.linalg.norm(v)+1e-9)
BACK,UP,AHEAD,NEAR=3.4,1.7,6.0,0.25

_last_r=[np.array([1.,0.,0.])]
def cam_at(i):
    p=line[i]; a=max(i-3,0); b=min(i+3,len(line)-1); t=nz(line[b]-line[a])
    cam=p-t*BACK+WUP*UP; tgt=p+t*AHEAD+WUP*0.4
    f=nz(tgt-cam)
    raw_r=np.cross(f,WUP)
    if np.linalg.norm(raw_r)<0.15:   # flight direction too close to vertical (WUP) — cross(f,WUP) degenerates and the camera roll flips upside down
        r=nz(_last_r[0]-f*np.dot(_last_r[0],f))   # hold the previous right-vector, re-orthogonalized against the new forward, instead of flipping
    else:
        r=nz(raw_r)
    _last_r[0]=r
    u=np.cross(r,f)
    return cam,np.array([r,u,f])

LAB=[(0,"Launch off the H"),(3,"360 the red marker  ·  CCW"),(11,"Up and over the bridge"),
     (14,"Across the top, past the bushes"),(16,"Left through the gemfan / cube gate"),
     (18,"Down between the wall & the pillar"),(21,"360 the green marker  ·  CW"),
     (28,"Back toward the red marker"),(31,"Duck UNDER the bridge"),
     (36,"Thread the hoop  ·  top → down"),(40,"Across to the ladder gate"),
     (42,"Weave the ladder  ·  top → bottom"),(59,"Finish — back through the H")]
def label_for(i):
    wp=i/16.; cur=LAB[0][1]
    for k,s in LAB:
        if wp>=k: cur=s
    return cur

FR=OUT+"/fly"; os.makedirs(FR,exist_ok=True)
NF=600; idxs=np.linspace(0,len(line)-1,NF).astype(int)
for fi,i in enumerate(idxs):
    cam,Rm=cam_at(i)
    d=tri-cam
    xc=d@Rm[0]; yc=d@Rm[1]; zc=d@Rm[2]
    infront=(zc>NEAR).all(axis=1)
    with np.errstate(divide='ignore',invalid='ignore'):
        sx=xc/zc; sy=yc/zc
    depth=zc.mean(1); shade=0.42+0.58*np.clip(np.abs(nrm@light),0,1)
    fc=col.copy(); wpn=i/16.                                   # hoop GLOWS only during the hoop pass
    fc[cyanmask]= np.clip(CYAN*1.7+0.22,0,1) if (29<=wpn<=40) else CYAN*0.38
    af=np.ones(len(col))                                      # per-face opacity (RGBA alpha)
    af[cyanmask]=np.clip(0.05+0.95*(wpn-18.75)/1.5,0.05,1.0)  # hoop 95% hidden until mark 6 (pillar, ~wp18.75) is crossed, then fades in
    order=np.argsort(-depth)
    polys=[]; cols=[]
    for j in order:
        if infront[j]:
            polys.append(np.column_stack([sx[j],sy[j]]))
            cols.append(np.append(np.clip(fc[j]*shade[j],0,1),af[j]))
    fig,ax=plt.subplots(figsize=(9.6,6.4)); fig.patch.set_facecolor("#0e0f13"); ax.set_facecolor("#0a0b0f")
    ax.add_collection(PolyCollection(polys,facecolors=cols,edgecolors="none",antialiased=True))
    seg=line[i:min(i+55,len(line))]; ds=seg-cam; sz2=ds@Rm[2]; mS=sz2>NEAR   # ONLY the immediate move is drawn
    if mS.sum()>1:
        ax.plot((ds@Rm[0])[mS]/sz2[mS],(ds@Rm[1])[mS]/sz2[mS],color="#d9b8ff",lw=3.8,alpha=0.98,zorder=8)
    dp=line[i]-cam; pz=dp@Rm[2]
    if pz>NEAR: ax.plot([dp@Rm[0]/pz],[dp@Rm[1]/pz],marker="o",ms=7,mfc="#fff",mec="#b06cff",mew=2,zorder=7)
    ax.text(0,0.55,label_for(i),color="#fff",fontsize=14,ha="center",weight="bold")
    ax.text(-0.87,-0.55,"TRACK 3 · lap 1",color="#b06cff",fontsize=10,ha="left",weight="bold")
    ax.text(0.87,-0.55,f"{int(100*fi/(NF-1))}%",color="#9aa0aa",fontsize=10,ha="right",weight="bold")
    ax.set_xlim(-0.9,0.9); ax.set_ylim(-0.6,0.6); ax.axis("off")
    plt.savefig(f"{FR}/f{fi:04d}.png",dpi=100,facecolor="#0e0f13"); plt.close()
    if fi%50==0: print("frame",fi,"/",NF)

mp4=OUT+"/track3-flythrough.mp4"
subprocess.run(["ffmpeg","-y","-framerate","15.3","-i",f"{FR}/f%04d.png",
   "-vf","scale=960:640:flags=lanczos","-c:v","libx264","-pix_fmt","yuv420p","-crf","20",mp4],
   check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
print("wrote",mp4)
