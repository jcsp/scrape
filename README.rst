
Setup
-----

If you already have PyYAML installed (e.g. deb package python-yaml) then nothing
is needed.  Otherwise:

::

    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt

Usage
-----

::

    python ./scrape.py <suite output>

Example
-------

::

    python ./scrape.py /a/john-2014-08-25_02:37:45-rados-wip-objecter-testing-basic-multi/

    Found 574 jobs
    Found 5 distinct failure reasons
    Dead: 2014-08-24T20:57:53.535 INFO:teuthology.orchestra.run.plana48.stderr:2014-08-24 20:57:53.507176 7f54b3850700  1 librados: shutdown
    ['447715']

    Failure: could not read lock status for ubuntu@plana25.front.sepia.ceph.com
    ['448052']

    Dead: 2014-08-24T20:57:48.575 INFO:teuthology.task.internal:waiting for more machines to be free (need 2 see 5)...
    ['447673', '447718']

    Assertion: osd/OSD.h: 1608: FAILED assert(peering_queue.empty())
    ceph version 0.84-678-ga67421a (a67421a5de5d94ec6953421fa142b5f239af9a94)
     1: (ceph::__ceph_assert_fail(char const*, char const*, int, char const*)+0x7f) [0xa9a01f]
     2: ceph-osd() [0x671342]
     3: (ThreadPool::stop(bool)+0x1a5) [0xa886e5]
     4: (OSD::shutdown()+0xb08) [0x62eec8]
     5: (OSD::handle_signal(int)+0xf6) [0x630146]
     6: (SignalHandler::entry()+0xfb) [0x9b278b]
     7: (()+0x7e9a) [0x5288e9a]
     8: (clone()+0x6d) [0x690e3fd]
    ['448053']

    Dead: 2014-08-24T20:57:53.769 INFO:tasks.ceph.mon.c:Stopped
    ['447683']
