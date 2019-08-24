# stricttuple

Python tuples with built in rule enforcement.

[![Downloads](https://pepy.tech/badge/stricttuple)](https://pepy.tech/project/stricttuple)
[![Downloads](https://pepy.tech/badge/stricttuple/month)](https://pepy.tech/project/stricttuple)
[![Downloads](https://pepy.tech/badge/stricttuple/week)](https://pepy.tech/project/stricttuple)
[![Known Vulnerabilities](https://snyk.io//test/github/CodyKochmann/stricttuple/badge.svg?targetFile=requirements.txt)](https://snyk.io//test/github/CodyKochmann/stricttuple?targetFile=requirements.txt)

## How to install it?

```
pip install stricttuple
```

This library is designed to restrict the inputs of your code by limiting what
the variables can become. This way, you'll know the full scope of what your code
is capable of messing up.

## Example Usage:

```python
In [1]: from stricttuple import stricttuple

In [2]: Point = stricttuple(
   ...:     "Point",
   ...:     x = (
   ...:          lambda x:type(x)==int,
   ...:          lambda x:x<15 and x>=0
   ...:     ),
   ...:     y = (
   ...:          lambda y:type(y)==int,
   ...:          lambda y:y<15 and y>=0
   ...:     )
   ...: )
```
This creates read only `Point` objects with two fields (x and y) that can only legally
be generated if the values of x and y are ints and between 0 and 15.
```
In [3]: Point(x=5, y=6)
Out[3]:
+---+---+
| x | 5 |
| y | 6 |
+---+---+
```
So, what happens if we assign `x` to the string `"fish"`?
```
In [4]: Point(x='fish', y=6)
---------------------------------------------------------------------------
IllegalStrictTuple                        Traceback (most recent call last)
<ipython-input-4-040e8d8fa069> in <module>
----> 1 Point(x='fish', y=6)

~/py3/lib/python3.6/site-packages/stricttuple/__init__.py in __call__(self, **kwargs)
    243                         type(v).__name__,
    244                         repr(v),
--> 245                         getsource(r).strip()
    246                         ))
    247         nt = self.namedtuple(**kwargs)

IllegalStrictTuple:
------------------------------------
instruction:
	Point.x = str('fish')
violates the rule:
	lambda x:type(x)==int,
------------------------------------
```

An `IllegalStrictTuple` exception is raised along with pinpointing what rule the input violated.

This means we can have debuggable data validation beyond just type checking like the following:

```
In [5]: Point(x=21, y=6)
---------------------------------------------------------------------------
IllegalStrictTuple                        Traceback (most recent call last)
<ipython-input-5-d943248369f4> in <module>
----> 1 Point(x=21, y=6)

~/py3/lib/python3.6/site-packages/stricttuple/__init__.py in __call__(self, **kwargs)
    243                         type(v).__name__,
    244                         repr(v),
--> 245                         getsource(r).strip()
    246                         ))
    247         nt = self.namedtuple(**kwargs)

IllegalStrictTuple:
------------------------------------
instruction:
	Point.x = int(21)
violates the rule:
	lambda x:x<15 and x>=0
------------------------------------
```
