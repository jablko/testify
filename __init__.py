# Workaround, http://www.python.org/dev/peps/pep-3130/
config = { 'count': 0, 'test': [] }

def equal(actual, expect):
  config['count'] += 1

  condition = expect == actual

  print 'PASS' if condition else 'FAIL "%s" "%s"' % (actual, expect)

  return condition

def expect(count):
  config['expect'] = count

def ok(*args):
  config['count'] += 1

  try:
    condition, actual = args

  except ValueError:
    condition = True

  print 'PASS' if condition else 'FAIL "%s"' % actual

  return condition

def test(decorated):
  config['test'].append(decorated)

  return decorated
