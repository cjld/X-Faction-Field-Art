import json
import cv2
from matplotlib import pylab as pl
import numpy as np
import random

def sqr(x): return x*x

def get_matrix(a1, a2, b1, b2):
    def get_arr(a1,a2):
        a1 = np.array(a1).squeeze()
        a2 = np.array(a2).squeeze()
        a3 = a1-a2
        a3 = np.array([-a3[1], a3[0]]) + a1
        return np.float32([a1,a2,a3]).squeeze()

    a = get_arr(a1,a2)
    b = get_arr(b1,b2)

    return cv2.getAffineTransform(a,b)

def transfer(M, a):
    a = np.concatenate([np.array(a).squeeze(),[1]])
    return np.matrix(M)*a.reshape([3,1])


def get_close(p1, p2):
    pr = []
    error = 0
    for i,p in enumerate(p1):
        p = np.array(p).squeeze()
        if i<4:
            pp = p
        else:
            pp = p2[0]
            for py in p2:
                if np.linalg.norm(p-pp,2) > np.linalg.norm(p-py,2):
                    pp = py
        pr.append(np.array(pp).squeeze())
        error = np.linalg.norm(p-pp,2) + error
    return np.array(pr), error

def get_transfer(p1, p2, d1, d2, iters, rg):
    min_error = 1e30
    res1 = []
    res2 = []
    for i in range(iters):
        a = random.randint(0,len(p2)-1)
        b = random.randint(0,len(p2)-1)
        if a==b: continue
        sk = np.linalg.norm(p2[a] - p2[b], 2)
        if sk > rg: continue
        M = get_matrix(d1,d2, p2[a], p2[b])
        pp1 = [transfer(M,p) for p in p1]
        pn1, error = get_close(pp1, p2)
        error = error / sk
        if error < min_error:
            res1 = pp1
            res2 = pn1
            min_error = error
        print "iter", i, "min error", min_error, "error", error, "sk", sk
    return np.array(res1).squeeze(), np.array(res2).squeeze()

def plot_with_edge(v, e):
    pl.plot(v[:,0], v[:,1], "o")
    for ee in e:
        pl.plot(v[ee,0], v[ee,1], "g")

enl = json.load(open("./../enlightened_alt.json"))
res = json.load(open("./../resistance_alt.json"))

portals = json.load(open("./portals.json"))

center = {"lat":39.999587,"lng":116.335799}

portals = sorted(portals,
    key=lambda x:
        sqr(x["LatLng"]["lat"] - center["lat"]) +
        sqr(x["LatLng"]["lng"] - center["lng"])
    )

ps = [[p["LatLng"]["lat"], p["LatLng"]["lng"]] for p in portals[:1000]]
ps = np.array(ps)

enl_p = np.array(enl['v'])[:,0:2]
res_p = np.array(res['v'])[:,0:2]
#enl_pr1, enl_pr2 = get_transfer(enl_p, ps, enl_p[4], enl_p[5])
res_pr1, res_pr2 = get_transfer(res_p, ps, res_p[4], res_p[5], 1000, 5e-3)
enl_pr1, enl_pr2 = get_transfer(enl_p, ps, enl_p[4], enl_p[5], 300, 1e-2)



pl.plot(ps[:,0], ps[:,1], "go")
#plot_with_edge(enl_pr1, enl['e'])
plot_with_edge(enl_pr2, enl['e'])
plot_with_edge(res_pr2, res['e'])
pl.axis('equal')
pl.show()

#enl_p = get_transfer(enl_p, ps)
#res_p = get_transfer(enl_p, ps)
