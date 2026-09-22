def solve(n:int, matrix: list[list[int]]) -> int:
    def _print_matrix()->None:
        for row in matrix:
            print(row)

    res = 0
    #print(matrix)

    for j in range(n):
        for i in range(n):
            if n % 2 == 1 and j == n // 2 and i == n // 2:
                continue
            count = (matrix[j][i] == matrix[n-1-j][n-1-i]) + (matrix[j][i] == matrix[n-1-i][j])  + (matrix[j][i] == matrix[i][n-1-j])

            if count == 3:
                continue
            elif count == 2:
                # Replacing all with the same value, even if 2 are already the same
                matrix[n-1-j][n-1-i] = matrix[j][i]
                matrix[n-1-i][j] = matrix[j][i]
                matrix[i][n-1-j] = matrix[j][i]
                #print("Here", j, i, 1)
                res += 1
            elif count == 1:
                # Replacing all with the same value, even if 1 is already the same
                # print(matrix[j][i], matrix[n-1-j][n-1-i], matrix[n-1-i][j], matrix[i][n-1-j])
                matrix[n-1-j][n-1-i] = matrix[j][i]
                matrix[n-1-i][j] = matrix[j][i]
                matrix[i][n-1-j] = matrix[j][i]
                #print("Here", j, i, 2)
                res += 2
            else:
                # We replace THIS element with its opposite to make all four equal
                matrix[j][i] = matrix[n-1-j][n-1-i]
                #print("Here", j, i, 3)
                res += 1
        
        # _print_matrix()

            #print("Element", matrix[j][i])
            #print("Opposite", matrix[n-1-i][n-1-j])
            #print("Left Rotating", matrix[n-1-j][i])
            #print("Right Rotating", matrix[j][n-1-i])

    return res


if __name__ == '__main__':
    t = int(input().strip())
    for _ in range(t):
        n =  int(input().strip())
        matrix = [[int(x) for x in input().strip()] for _ in range(n)]
        print(solve(n, matrix))