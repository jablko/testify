import os, re, sys, traceback

__all__ = 'equal', 'expect', 'ok', 'test'

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
