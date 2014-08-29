# BEGIN_COPYRIGHT
# 
# Copyright 2009-2014 CRS4.
# 
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
# 
# END_COPYRIGHT

"""
This module allows you to write the components of your MapReduce application.

The basic MapReduce components (Mapper, Reducer, RecordReader, etc.)
are provided as abstract classes. Application developers must subclass
them, providing implementations for all methods called by the
framework.

**NOTE:** this module is provided only for backward compatibility support. If you are writing new code, use the api
defined in `pydoop.mapreduce.api`
"""

import pydoop.mapreduce.api
from pydoop.mapreduce.pipes import Factory
from pydoop.mapreduce.api import Mapper, Reducer, RecordReader, RecordWriter, Partitioner
from pydoop.mapreduce.pipes import run_task as runTask, InputSplit


class RecordReaderWrapper(object):
    def __init__(self, obj):
        self._obj = obj

    def next(self):
        flag, key, value = self._obj.next()
        if flag:
            return (key, value)
        else:
            raise StopIteration

    def __iter__(self):
        return self


class RecordReader(pydoop.mapreduce.api.RecordReader):
    """
  Breaks the data into key/value pairs for input to the :class:`Mapper`\ .
  """

    def __init__(self, context=None):
        super(RecordReader, self).__init__(context)

    def next(self):  # FIXME, different interface from api, needed
        """
    Called by the framework to provide a key/value pair to the
    :class:`Mapper`\ . Applications must override this.

    :rtype: tuple
    :return: a tuple of three elements. The first one is a bool which
      is True if a record is being read and False otherwise (signaling
      the end of the input split). The second and third element are,
      respectively, the key and the value (as strings).
    """
        raise NotImplementedError

    def __iter__(self):
        return RecordReaderWrapper(self)

    def get_progress(self):
        return self.getProgress()

    def getProgress(self):
        raise NotImplementedError


class Combiner(Reducer):
    """
    Works exactly as a :class:`Reducer`\ , but values aggregation is performed
    locally to the machine hosting each map task.
    """