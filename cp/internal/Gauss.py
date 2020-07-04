def gaussMethod(A, b, EPS=1e-6):
    n = len(A)
    m = len(A[0])
    where = [-1 for x in range(m)]
    col = 0
    row = 0
    while col<m and row<n :
        sel = row
        for i in range(row, n) :
            if (abs(A[i][col]) > abs(A[sel][col])) :
                sel = i
        if (abs(A[sel][col]) < EPS) :
            col += 1
            continue
        for i in range(col, m) :
            A[sel][i], A[row][i] = A[row][i], A[sel][i]
        b[sel], b[row] = b[row], b[sel]
        where[col] = row

        for i in range(n) :
            if i != row :
                c = A[i][col] / A[row][col]
                for j in range(col, m) :
                    A[i][j] -= A[row][j] * c
                b[i] -= b[row] * c
        col += 1
        row += 1
    ans = [0 for x in range(m)]
    for i in range (m) :
        if where[i] != -1 :
            ans[i] = b[where[i]] / A[where[i]][i]
    return ans
