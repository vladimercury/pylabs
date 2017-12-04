def list_sum(lst):
    def part_sum(tail):
        def _(s):
            return s if len(tail) == 0 else part_sum(tail[1:])(s + tail[0])
        return _
    return part_sum(lst)(0)


def insertions(elem):
    def _(lst):
        return [[elem]] if len(lst) == 0 \
            else [[elem] + lst] + list(map(lambda z: [lst[0]] + z, insertions(elem)(lst[1:])))
    return _
