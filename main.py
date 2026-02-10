from matrices import Matrix

A = Matrix.from_type(3, 3) \
    .fill(0, lambda r, c: r != c) \
    .fill(1, lambda r, c: r == c) ;  
# A(3x3) tal que:
# 1 se i == j;
# 0 se i != j;
print(A)
# [1, 0, 0]
# [0, 1, 0]
# [0, 0, 1]