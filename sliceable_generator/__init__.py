from itertools import islice
from typing import Iterable, TypeVar, Union, List, Generic

ChildType = TypeVar('ChildType')


class SliceableGenerator(Generic[ChildType]):
    """
    A generator supports reusing and slicing.
    Wrap a builtin generator to get more functions.

    Notes:
        This generator is a low performance implementation, compared with builtin generators.
        Read README.md for more information.
    """

    def __init__(self, data: Iterable[ChildType], depth=1):
        """Convert a generator to a new reusable and subscriptable generator.

        Args:
            data: any iterable object
            depth: depth of the iterator, default to 1
        """
        assert isinstance(depth, int) and depth > 0, 'depths should be a natural number'
        self.__depth = depth
        # Children have the lower depth
        self.__data = depth == 1 and (i for i in data) or (SliceableGenerator(i, depth=depth - 1) for i in data)
        self.__cached_data = []  # Cache iterated data for reusability.

    def __next__(self):
        raise NotImplementedError('Sliceable generator is reusable, so without inner state.')

    def __iter__(self) -> Iterable[ChildType]:
        yield from self.__cached_data
        yield from (self.__cached_data.append(datum) or datum for datum in self.__data)

    def __len__(self) -> int:
        return len([_ for _ in self])

    def __getitem__(self, item) -> Union['SliceableGenerator[ChildType]', ChildType]:
        # for slice, call standard library and return a new generator with the same depth
        if isinstance(item, slice):
            start, stop, step = item.start, item.stop, item.step
            if start is not None and start < 0:
                start += len(self)
            if stop is not None and stop < 0:
                stop += len(self)
            return SliceableGenerator(islice(self, start, stop, step), depth=self.__depth)

        # For int, operate as it is an index
        elif isinstance(item, int):
            if item < 0:
                if item + len(self) < 0:
                    raise IndexError(str(item))
                item = item + len(self)
            # TODO Check if in the cache, if not then call iter(self)
            g = iter(self)
            try:
                [next(g) for _ in range(item)]
                return next(g)
            except StopIteration:
                raise IndexError(item)

        # For tuple type, if length is 1, then simply call recursively;
        # if length > 1, apply the first param to self and other params to children
        elif isinstance(item, tuple):
            assert self.__depth >= len(item), 'Slice depth larger than generator depth'
            assert len(item) > 0, 'empty tuple not supported'
            if len(item) == 1:
                return self[item[0]]
            assert all(isinstance(i, (slice, int)) for i in item), f'({", ".join(type(i).__name__ for i in item)})'
            first_param, extra_param = item[0], item[1:]
            # if the first param is instance of int, return the next layer; if is instance of slice, return same layer
            if isinstance(first_param, int):
                return self[first_param][extra_param]
            else:
                # For tuple param, if it contains some integer indexes, then the layer for such indexes will vanished.
                depth = self.__depth - [isinstance(i, int) for i in extra_param].count(True)
                return SliceableGenerator((i[extra_param] for i in self[first_param]), depth=depth)
        else:
            raise TypeError(type(item).__name__)

    def to_list(self) -> List[List, ChildType]:
        return list(self) if self.__depth == 1 else [i.to_list() for i in self]

    def __repr__(self):
        return f'{self.__class__.__name__}[cached: {", ".join(map(str, self.__cached_data))}]'


__version__ = '0.1.1'
__author__ = 'panhaoyu'
__email__ = 'panhaoyu.china@outlook.com'

if __name__ == '__main__':
    import doctest

    doctest.testmod()
