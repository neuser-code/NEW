m = [[x for x in range(0,16)] for k in range(0, 16)]
k = 0
for i in range(0, 16):
	for d in range(0,16):
		m[i][d] = [k, (0,0,0)]
		k += 1

for t in range(0, 16):
	if t % 2 != 0:
		m[t].reverse()

#for k in range(0,16):
#    for i in range(0,16):
#        pix[m[k][i][0]] = m[k][i][1]
