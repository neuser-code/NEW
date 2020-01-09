m = [[x for x in range(0,16)] for k in range(0, 16)]
k = 0
for i in range(0, 16):
	for d in range(0,16):
<<<<<<< HEAD
		m[i][d] = [k, (0,0,0)]
=======
		m[i][d] = k
>>>>>>> acc58e7ccb0ca04ab8f10faf113675a0f48c1e23
		k += 1

for t in range(0, 16):
	if t % 2 != 0:
		m[t].reverse()

<<<<<<< HEAD
#for k in range(0,16):
#    for i in range(0,16):
#        pix[m[k][i][0]] = m[k][i][1]
=======
>>>>>>> acc58e7ccb0ca04ab8f10faf113675a0f48c1e23
