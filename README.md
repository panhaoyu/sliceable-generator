# sliceable-generator: Powerful generator for Python

In python, generators are designed for one-time use,
zero space complexity, lazy computation collection.

However, sometimes we need a lazy computation list,
with the capability to index, slice and reuse,
which is the propose of this package.

## Installation

```shell script
pip install sliceable-generator
```

## Usage

Sliceable generator aims to provide the same experience as builtin generators, but more powerful.
So, simply wrap the builtin generators is ok.

```python
from sliceable_generator import SliceableGenerator
g = SliceableGenerator(range(300, 400))
for i in g[50:53]:
    print(i)
# 350
# 351
# 352
```

### Nested generators

Pay attention that python builtin generators will perform unexpected when nested.
The parent variable will not pass to child generators.

```python
g = (((i, j) for j in range(20, 30)) for i in range(10, 20))
sub1, sub2, sub3 = next(g), next(g), next(g)
print(list(sub2))
# [(12, 20), (12, 21), (12, 22), (12, 23), (12, 24), (12, 25), (12, 26), (12, 27), (12, 28), (12, 29)]
print(list(sub1))
# [(12, 20), (12, 21), (12, 22), (12, 23), (12, 24), (12, 25), (12, 26), (12, 27), (12, 28), (12, 29)]
```

Sliceable generator will not operate such case, so if you use nested generators,
please manage your generator like such code: 

```python
g = ((lambda i: ((i, j) for j in range(20, 30)))(i) for i in range(10, 20))
sub1, sub2, sub3 = next(g), next(g), next(g)
print(list(sub2))
# [(11, 20), (11, 21), (11, 22), (11, 23), (11, 24), (11, 25), (11, 26), (11, 27), (11, 28), (11, 29)]
print(list(sub1))
# [(10, 20), (10, 21), (10, 22), (10, 23), (10, 24), (10, 25), (10, 26), (10, 27), (10, 28), (10, 29)]
```

Thanks to QQ user `村长` for providing this solution. 

If provided correct nested generator, wrap it with `SliceableGenerator`:

```python
from sliceable_generator import SliceableGenerator
g = SliceableGenerator(((lambda i: ((i, j) for j in range(20, 30)))(i) for i in range(10, 20)), depth=2)
print(g[3:5, 4:6].to_list())
# [[(13, 24), (13, 25)], [(14, 24), (14, 25)]]
print(g[3:5, 4].to_list())
# [(13, 24), (14, 24)]
```

## Attention

Pay attention that this package provide a low performance generator implementation.
Only when you need both lazy computation and subscript functions,
you can use this package.
Otherwise, use builtin generator expressions instead. 

## Contribution

This is a tiny package and if you want to contribute, just raise a pull request,
and any proposals are welcome!

## History

* v0.1.0: finish basic logic
    * length of generator
    * reusable generator
    * sliceable generator
    * subscriptable generator
    * nested generator