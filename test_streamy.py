import json, streamy, unittest, io


class StreamyTest(unittest.TestCase):
    def _stream(self, s):
        return streamy.stream(s)

    def assert_stream(self, s, *expected):
        return self.assertEqual(list(self._stream(s)), list(expected))

    def stream_fails(self, s):
        with self.assertRaises(ValueError):
            list(streamy.stream(s))

    def test_empty(self):
        for s in '', ' ', '   ', '\n \n ':
            self.assert_stream(s)

    def test_reserved(self):
        RESERVED = {'true': True, 'false': False, 'null': None, '12': 12}
        for k, v in RESERVED.items():
            self.assert_stream(k, v)
        self.assert_stream('null false true 12.5', None, False, True, 12.5)

    def test_objects(self):
        self.assert_stream('{} {"foo": 1, "bar": true}',
                           {}, {"foo": 1, "bar": True})

    def test_lists(self):
        self.assert_stream(' [   ]    ["foo", 1, "bar", null]  ',
                           [], ["foo", 1, "bar", None])

    def test_error(self):
        self.stream_fails(']')
        self.stream_fails('[}')
        self.stream_fails('}')
        self.stream_fails('2,,')
        self.stream_fails('[2,]')


class NotSeekableTest(StreamyTest):
    def _stream(self, s):
        fp = io.StringIO(s)
        fp.seekable = lambda: False
        return streamy.stream(fp)
