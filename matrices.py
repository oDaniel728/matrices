from typing import Any, Callable, Generator, Iterator, Self, TypedDict, overload


type matrix_list[T] = list[list[T]]
type real = int | float

class MatrixRow:
    def __init__(self, matrix: 'Matrix', row: int) -> None:
        self._matrix = matrix
        self._row = row

    def __list__(self) -> list[real]:
        return self._matrix._matrix[self._row]

    def __tuple__(self) -> tuple[real, ...]:
        return tuple(self.__list__())
    
    def __iter__(self) -> Iterator[real]:
        return iter(self.__list__())
    
    def __repr__(self) -> str:
        # [ a1 a2 a3 ]
        return f"[ {' '.join([str(i) for i in list(self)])} ]"
    
    def __getitem__(self, key: int) -> real:
        return list(self)[key]
    
    def __setitem__(self, key: int, value: real) -> None:
        self._matrix._matrix[self._row][key] = value

    def fill(self, value: real, rule: Callable[[int], bool]) -> None:
        for i, v in enumerate(self):
            if rule(i): self[i] = value

    def eval(self, rule: Callable[[tuple[int, real], real], real]) -> None:
        for i, v in enumerate(self):
            self[i] = rule((i, v), v)
    
class MatrixDimentions(TypedDict):
    lines: int
    columns: int

class Matrix:
    def __init__(self, matrix: matrix_list[real]) -> None:
        self._matrix = matrix

    @property
    def dimentions(self) -> MatrixDimentions:
        return MatrixDimentions({
            'lines': len(self._matrix), 
            'columns': len(self._matrix[0])
        })

    def __repr__(self) -> str:
        l, c = self.dimentions
        return f"Matrix {l}x{c}"
    
    def __iter__(self):
        return iter(self.__list__())
    
    def __list__(self) -> list[MatrixRow]:
        return [MatrixRow(self, i) for i, _ in enumerate(self._matrix)]
    
    def __tuple__(self) -> tuple[tuple[real, ...], ...]:
        return tuple(tuple(row) for row in list(self))
    
    @overload
    @staticmethod
    def from_type(lines: int, columns: int) -> 'Matrix': ...
    @overload
    @staticmethod
    def from_type(lines: int, columns: int, value: real) -> 'Matrix': ...

    @staticmethod
    def from_type(lines: int, columns: int, value: real = 0) -> 'Matrix':
        return Matrix([[value for _ in range(columns)] for _ in range(lines)])
    
    @staticmethod
    def from_order(order: int, value: real = 0) -> 'Matrix':
        return Matrix.from_type(order, order, value)
    
    @staticmethod
    def from_identity(order: int) -> 'Matrix':
        m = Matrix.from_order(order)
        for i in range(order):
            m[i][i] = 1
        return m
    
    def __getitem__(self, key: int) -> MatrixRow:
        return MatrixRow(self, key)
    
    def __setitem__(self, key: int, value: list[real]) -> None:
        for i, v in enumerate(value):
            self[key][i] = v
    
    def is_square(self) -> bool:
        return self.dimentions['lines'] == self.dimentions['columns']
    
    def foreach(self) -> Generator[real, None, None]:
        for r in self:
            for c in r:
                yield c
        return
    
    def foreach_pos(self) -> Generator[tuple[int, int], None, None]:
        for r in range(self.dimentions['lines']):
            for c in range(self.dimentions['columns']):
                yield r, c
        return
    
    def is_null(self) -> bool:
        for c in self.foreach():
            if c != 0:
                return False
        return True
    
    def count_values(self) -> dict[real, int]:
        counts = {}
        for c in self.foreach():
            if c not in self.count_values():
                counts[c] = 1
            else:
                counts[c] += 1
        return counts
    
    def is_identity(self) -> bool:
        if not self.is_square(): return False
        if self.count_values().keys() == {0, 1}: return True

        for (r, c) in self.foreach_pos():
            if r == c and self[r][c] != 1: return False
            if r != c and self[r][c] != 0: return False

        return False
    
    def fill(self, value: real, rule: Callable[[int, int], bool]) -> Self:
        for (r, c) in self.foreach_pos():
            if rule(r, c): self[r][c] = value
        return self

    def eval(self, rule: Callable[[tuple[int, int], real], real]) -> Self:
        for (r, c) in self.foreach_pos():
            self[r][c] = rule((r, c), self[r][c])
        return self

    def __add__(self, other: 'Matrix') -> "Matrix":
        if self.dimentions != other.dimentions: raise ValueError("Matrices must be the same size")
        res = Matrix.from_type(**self.dimentions)
        for (r, c) in self.foreach_pos():
            res[r][c] = self[r][c] + other[r][c]
        return res
    
    def __iadd__(self, other: 'Matrix'):
        return self + other
    
    def __sub__(self, other: 'Matrix') -> "Matrix":
        if self.dimentions != other.dimentions: raise ValueError("Matrices must be the same size")
        res = Matrix.from_type(**self.dimentions)
        for (r, c) in self.foreach_pos():
            res[r][c] = self[r][c] - other[r][c]
        return res
    
    def __isub__(self, other: 'Matrix'):
        return self - other

    def __neg__(self):
        return self.eval(lambda pos, v: -v)