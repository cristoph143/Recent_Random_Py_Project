class one:
    def __init__(self, app):
        self.app = app


num = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [[1, 2, 3], 1]
]
for row in num:
    for col in row:
        print(col)
