m = [[x for x in range(0,16)] for k in range(0, 16)]
k = 0
for i in range(0, 16):
	for d in range(0,16):
		m[i][d] = k
		k += 1

for t in range(0, 16):
	if t % 2 != 0:
		m[t].reverse()

