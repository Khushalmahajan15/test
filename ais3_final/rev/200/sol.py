ans = [0 for i in range(61)]
ans[59] = 1
ans[60] = 1
for i in range(58, -1, -1):
    for j in range(i + 1, i + 38):
        if j > 60:
            break
        else:
            ans[i] += ans[j]

print ans[0]

    
