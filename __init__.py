import os, re, sys, traceback

__all__ = 'equal', 'equiv', 'expect', 'ok', 'test'

def equal(expect, actual):
  current.count += 1

  condition = expect == actual
  if condition:
    #print 'ok {!r}'.format(current.count)
    print 'ok {0!r}'.format(current.count)

  else:
    #print 'not ok {!r}'.format(current.count)
    print 'not ok {0!r}'.format(current.count)
    #print re.sub('^', '# ', repr(actual), flags=re.M)
    print re.compile('^', re.M).sub('# ', repr(actual))
    #print re.sub('^', '# ', repr(expect), flags=re.M)
    print re.compile('^', re.M).sub('# ', repr(expect))

    traceback.print_stack(sys._getframe().f_back, file=sys.stdout)

  return condition

def equiv(expect, actual):
  current.count += 1

  def equiv(expect, actual, condition):
    if expect is actual:
      return condition

    # Strings are recursive, 'a' == 'a'[0] == 'a'[0][0], etc. but equivalent
    # strings are identical, 'a' is 'a'.  Strings are common and we can't
    # determine nonequivalence without this special case.  Could this case be
    # more general, like recursive values are nonequivalent unless identical?
    # What about a = [], a.append(a), b = [], b.append(b), equiv(a, b)?  Maybe
    # they're equivalent because they both reference themselves? but then 'a'
    # and 'b' - and hence all equal length strings - are equivalent : (
    if isinstance(actual, str) or not isinstance(actual, type(expect)):
      if condition:
        #print 'not ok {!r}'.format(current.count)
        print 'not ok {0!r}'.format(current.count)

      #print re.sub('^', '# ', repr(actual), flags=re.M)
      print re.compile('^', re.M).sub('# ', repr(actual))
      #print re.sub('^', '# ', repr(expect), flags=re.M)
      print re.compile('^', re.M).sub('# ', repr(expect))

      return False

    try:
      return equiv(expect.__dict__, actual.__dict__, condition)

    except AttributeError:
      try:

        # Without **, ((1, 2), (3, 4)) and ((3, 4), (1, 2)) would be
        # equivalent, and 'abc' would raise ValueError
        expect = dict(**expect)
        actual = dict(**actual)

      except TypeError:
        try:
          expect = iter(expect)
          actual = iter(actual)

        except TypeError:
          if condition:
            #print 'not ok {!r}'.format(current.count)
            print 'not ok {0!r}'.format(current.count)

          #print re.sub('^', '# ', repr(actual), flags=re.M)
          print re.compile('^', re.M).sub('# ', repr(actual))
          #print re.sub('^', '# ', repr(expect), flags=re.M)
          print re.compile('^', re.M).sub('# ', repr(expect))

          return False

        while True:
          try:
            condition = equiv(expect.next(), actual.next(), condition)

          except StopIteration:
            break

        for itm in actual:
          if condition:
            #print 'not ok {!r}'.format(current.count)
            print 'not ok {0!r}'.format(current.count)

          #print re.sub('^', '# ', repr(itm), flags=re.M)
          print re.compile('^', re.M).sub('# ', repr(itm))

          condition = False

        for itm in expect:
          if condition:
            #print 'not ok {!r}'.format(current.count)
            print 'not ok {0!r}'.format(current.count)

          #print re.sub('^', '# ', repr(itm), flags=re.M)
          print re.compile('^', re.M).sub('# ', repr(itm))

          condition = False

        return condition

      for key in set(expect) & set(actual):
        condition = equiv(expect[key], actual[key], condition)

      for key in set(actual) - set(expect):
        if condition:
          #print 'not ok {!r}'.format(current.count)
          print 'not ok {0!r}'.format(current.count)

        #print re.sub('^', '# ', repr(actual[key]), flags=re.M)
        print re.compile('^', re.M).sub('# ', repr(actual[key]))

        condition = False

      for key in set(expect) - set(actual):
        if condition:
          #print 'not ok {!r}'.format(current.count)
          print 'not ok {0!r}'.format(current.count)

        #print re.sub('^', '# ', repr(expect[key]), flags=re.M)
        print re.compile('^', re.M).sub('# ', repr(expect[key]))

        condition = False

      return condition

  condition = equiv(expect, actual, True)
  if condition:
    #print 'ok {!r}'.format(current.count)
    print 'ok {0!r}'.format(current.count)

  else:
    traceback.print_stack(sys._getframe().f_back, file=sys.stdout)

  return condition

def expect(count):
  current.expect = count

  #print '1..{!r}'.format(count)
  print '1..{0!r}'.format(count)

def ok(condition, *args):
  current.count += 1

  if condition:
    #print 'ok {!r}'.format(current.count)
    print 'ok {0!r}'.format(current.count)

  else:
    #print 'not ok {!r}'.format(current.count)
    print 'not ok {0!r}'.format(current.count)

    try:
      #print re.sub('^', '# ', repr(*args), flags=re.M)
      print re.compile('^', re.M).sub('# ', repr(*args))

    except TypeError:
      pass

    traceback.print_stack(sys._getframe().f_back, file=sys.stdout)

  return condition

class test:
  def __init__(self, cbl):

    # Module scope?
    global current

    print '# ' + cbl.__name__

    self.count = 0

    cwd = os.getcwd()

    try:
      parent = current

    except NameError:
      pass

    current = self

    cbl()

    try:
      if self.expect != self.count:
        #print 'FAIL {!r} {!r}'.format(self.expect, self.count)
        print 'FAIL {0!r} {1!r}'.format(self.expect, self.count)

        traceback.print_stack(sys._getframe().f_back, file=sys.stdout)

    except AttributeError:
      pass

    try:
      current = parent

    # We're still current if we've no parrent

    # TODO Correct?
    except UnboundLocalError:
      pass

    os.chdir(cwd)

# Enables test scripts without runner, except "expect" verification

# TODO Drop?
test(lambda: None)
