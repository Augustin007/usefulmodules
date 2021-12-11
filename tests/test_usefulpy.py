from usefulpy import *
import pytest


### VALIDATION TEST ###
...

### MATHEMATICS TEST ###

## Basenum ##
def test_basenumlessthanten():
    test = mathematics.basenum('---1010', 2)
    assert test.base == 2
    assert test.num == '1010'
    assert test.floatpart == ''
    assert test.Negative == True

def test_basenumlessthanten1():
    test = mathematics.basenum('1010.1', 3)
    assert test.base == 3
    assert test.num == '1010'
    assert test.floatpart == '1'
    assert test.Negative == False

## Mathfuncs ##
def test_mathfunc_add():
    cos=mathematics.cos
    assert cos+cos == 2*cos

def test_mathfunc_sub():
    x = mathematics.x
    assert x-x == mathematics.trivial

def test_mathfunc_mul():
    x = mathematics.x
    cos = mathematics.cos
    assert x*x==x**2
    assert (x+cos)*x==x**2+x*cos

## nmath ##
def test_primality():
    assert mathematics.Prime(9999999999998999999999)
    assert not mathematics.Prime(9999999999999000000000)

## vector ##
def test_vector():
    ...

### FORMATTING TEST ###
...

### PY3d TEST ###
...
