import numpy as np


def unpack(field):
	
	
  iix = range(0,field.lr1[0],1) 
  nix = len(iix)        
  iiy = range(0,field.lr1[1],1) 
  niy = len(iiy)
  iiz = range(0,field.lr1[2],1) 
  niz = len(iiz)	
  nppel = nix*niy*niz
  nepel = (nix-1)*(niy-1)*max((niz-1),1)  
  nel   = field.nel*nepel
  if (field.ndim==3):
    nvert = 8
    #cellType = tvtk.Hexahedron().cell_type
  else:
    nvert = 4
		#cellType = tvtk.Quad().cell_type
  
  of = np.arange(0, nvert*nel, nvert)
  ce = np.zeros(nel*(nvert+1)) 
  ce[range(0,nel*(nvert+1),nvert+1)] = nvert
  #if (field.var[0]!=0):
    #r  = np.zeros((nvert*nel,3))
  if (field.var[1]!=0):
    v  = np.zeros((nvert*nel,3))
  if (field.var[2]==1):
    p  = np.zeros((nvert*nel))
  if (field.var[3]==1):
    T  = np.zeros((nvert*nel))
  if (field.var[4]!=0):
    S  = np.zeros((nvert*nel,field.var[4]))
  ice = -(nvert + 1)
  
  for iel in range(field.nel):
    for iz in range(niz):
      for iy in range(niy):
        for ix in range(nix):
          #if (field.var[0]==3):
            #r[iel*nppel + ix + iy*nix + iz*nix*niy,:] = field.elem[iel].pos [:, iiz[iz], iiy[iy], iix[ix]]

          if (field.var[1]==3):
            v[iel*nppel + ix + iy*nix + iz*nix*niy,:] = field.elem[iel].vel [:, iiz[iz], iiy[iy], iix[ix]]

          if (field.var[2]==1):
            p[iel*nppel + ix + iy*nix + iz*nix*niy]   = field.elem[iel].pres[:, iiz[iz], iiy[iy], iix[ix]]

#          if (field.var[3]==1):
#            T[iel*nppel + ix + iy*nix + iz*nix*niy]   = field.elem[iel].temp[:, iiz[iz], iiy[iy], iix[ix]]

#          if (field.var[4]!=0):
#            S[iel*nppel + ix + iy*nix + iz*nix*niy,:] = field.elem[iel].scal[:, iiz[iz], iiy[iy], iix[ix]]

                      
  return v, p
