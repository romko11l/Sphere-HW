class ImprovedList(list):
    def __add__(self, other):
        if len(self) == len(other):
            result = [x + y for x, y in zip(self, other)]
        elif len(self) < len(other):
            result = [x + y for x, y in zip(self, other[:len(other)])]
            for i in range(len(self), len(other)):
                result.append(other[i])
        elif len(self) > len(other):
            result = other + self
        return ImprovedList(result)

    def __sub__(self, other):
        temp_list = - other
        return self + temp_list

    def __neg__(self):
        result = ImprovedList([-i for i in self])
        return result

    def __pos__(self):
        return self

    def __lt__(self, other):
        return sum(self) < sum(other)

    def __gt__(self, other):
        return sum(self) > sum(other)

    # ToDo: допилить += -= и остальные сравнения


if __name__ == '__main__':
    pass
