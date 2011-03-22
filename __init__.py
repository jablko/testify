__all__ = ['equal', 'expect', 'ok', 'test']

def equal(actual, expect):
  current.count += 1

  condition = expect == actual

  print 'PASS' if condition else 'FAIL "%s" "%s"' % (actual, expect)

  return condition

def expect(count):
  current.expect = count

def ok(*args):
  current.count += 1

  try:
    condition, actual = args

  except ValueError:
    condition = True

  print 'PASS' if condition else 'FAIL "%s"' % actual

  return condition

class test:
  def __init__(self, decorated):

    # Module scope?
    global current

    self.count = 0

    try:
      self.parent = current

    except NameError:
      pass

    current = self

    decorated()

    try:
      if self.expect != self.count:
        print 'FAIL %s %s' % (self.expect, self.count)

    except AttributeError:
      pass

    try:
      current = self.parent

    # We're still current if we've no parrent

    # TODO Correct?
    except AttributeError:
      pass

# Enables test scripts without harness, except "expect" verification

# TODO Drop?
test(lambda: None)
