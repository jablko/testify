import functools, sys, traceback

__all__ = ['equal', 'expect', 'ok', 'test']

def equal(actual, expect):
  current.count += 1

  condition = expect == actual
  if condition:
    print 'ok %r' % current.count

  else:
    print 'not ok %r %r %r' % (current.count, actual, expect)

    traceback.print_stack(file=sys.stdout)

  return condition

def expect(count):
  current.expect = count

  print '1..%r' % count

def ok(condition, *args):
  current.count += 1

  if condition:
    print 'ok %r' % current.count

  else:
    try:
      actual, = args

      print 'not ok %r %r' % (current.count, actual)

    except ValueError:
      print 'not ok %r' % current.count

    traceback.print_stack(file=sys.stdout)

  return condition

class test:
  def __init__(self, decorated):

    # Module scope?
    global current

    functools.update_wrapper(self, decorated)

    self.count = 0

    try:
      self.parent = current

    except NameError:
      pass

    current = self

    decorated()

    try:
      if self.expect != self.count:
        print 'FAIL %r %r' % (self.expect, self.count)

        traceback.print_stack(file=sys.stdout)

    except AttributeError:
      pass

    try:
      current = self.parent

    # We're still current if we've no parrent

    # TODO Correct?
    except AttributeError:
      pass

# Enables test scripts without runner, except "expect" verification

# TODO Drop?
test(lambda: None)
