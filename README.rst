===========
makeTorrent
===========


A basic python library for generating single and multi-file torrents.


Usage
=====

Basic usage:

.. code-block:: python

    from makeTorrent import makeTorrent

    mk = makeTorrent(announce='http://example.com/announce')


At this point the makeTorrent class contains a dictionary, which can be printed either as a dict or as a bencoded string (torrent format).

To add files, use either the multi_file class or the single_file class:

.. code-block:: python

    mk.multi_file('/path/to/directory')

    with open('my.torrent') as tf:
        tf.write(mk.getBencoded())

The same method can be used with `mk.single_file` with just pointing out a single file.

Notes
=====

There are a number of items that can be added when initializing the class:

.. code-block:: python

    mk = makeTorrent(
        announce='http://example.com/announce',
        comment='Test Torrent',
        httpseeds=['http://example.com/file.iso'],
        announcelist=[['http://announce1.example.com'],['http://announce2.example.com']]
    )


