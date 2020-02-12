import ipdb
ipdb.set_trace()
ipdb.set_trace(context=5)  # will show five lines of code
# instead of the default three lines
ipdb.pm()
ipdb.run('x[0] = 3')
result = ipdb.runcall(function, arg0, arg1, kwarg='foo')
result = ipdb.runeval('f(1,2) - 3')
