# Tool to generate file tree with empty files based on real file tree.
# Copyright (C) 2019  Ivan Mironov <mironov.ivan@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import logging
import marshal
import os
import socket
import stat
import subprocess
import sys


_FAKEROOT = 'fakeroot'
_MKSQUASH = 'mksquashfs'
_SELF = 'fsholetree.puncher'


_LOG = logging.getLogger(__name__)


if sys.version_info[0] == 2:
    def _load_from_stdin(stdin):
        return marshal.load(stdin)
else:
    def _load_from_stdin(stdin):
        return marshal.load(stdin.buffer)


def _touch(full_path, size):
    with open(full_path, 'wb') as file_obj:
        os.ftruncate(file_obj.fileno(), size)


def _mksock(full_path):
    sock = socket.socket(socket.AF_UNIX)
    sock.bind(full_path)
    sock.close()


def _simplify_item(item):
    # Should be in sync with _create_hole().
    return item[0], (
        item[1].st_mode,
        item[1].st_uid,
        item[1].st_gid,
        item[1].st_rdev,
        item[1].st_size,
        item[1].st_atime,
        item[1].st_mtime,
    ), item[2]


def _create_hole(full_path, stat_data, link_path, deferred_dir_times):
    # Should be in sync with _simplify_item().
    (
        st_mode,
        st_uid,
        st_gid,
        st_rdev,
        st_size,
        st_atime,
        st_mtime,
    ) = stat_data

    # TODO: Add st_flags.
    # TODO: Add xattrs.

    if stat.S_ISDIR(st_mode):
        os.mkdir(full_path, stat.S_IMODE(st_mode))
        # Change atime/mtime later, after creating files inside directories.
        # Order should be reverse.
        deferred_dir_times.insert(0, (full_path, (st_atime, st_mtime)))
    elif stat.S_ISCHR(st_mode) or \
            stat.S_ISBLK(st_mode) or \
            stat.S_ISFIFO(st_mode):
        os.mknod(full_path, st_mode, st_rdev)
        os.utime(full_path, (st_atime, st_mtime))
    elif stat.S_ISLNK(st_mode):
        os.symlink(link_path, full_path)
    elif stat.S_ISSOCK(st_mode):
        _mksock(st_mode)
        os.chmod(full_path, stat.S_IMODE(st_mode))
        os.utime(full_path, (st_atime, st_mtime))
    elif stat.S_ISREG(st_mode):
        _touch(full_path, st_size)
        os.chmod(full_path, stat.S_IMODE(st_mode))
        os.utime(full_path, (st_atime, st_mtime))
    else:
        raise RuntimeError(
            'Type of \"{}\" is not supported (st_mode == 0o{:o})'.format(
                full_path,
                st_mode))

    os.lchown(full_path, st_uid, st_gid)


def _set_dir_times(deferred_dir_times):
    for full_path, times in deferred_dir_times:
        os.utime(full_path, times)


def _create_tree_process_inner(tree_path):
    deferred_dir_times = []
    while True:
        item = _load_from_stdin(sys.stdin)
        if item is None:
            break

        path, stat_data, link_path = item
        _create_hole(
            os.path.abspath(os.path.join(tree_path, path)),
            stat_data,
            link_path,
            deferred_dir_times)

    _set_dir_times(deferred_dir_times)


def _create_tree_process():
    conf = _load_from_stdin(sys.stdin)
    _create_tree_process_inner(**conf)


def _create_tree(items, fr_save_path, tree_path):
    cmd = [
        _FAKEROOT,
        '-s',  # save fake environment into file
        fr_save_path,
        '--',
        sys.executable,
        '-m',  # run python module
        _SELF,
    ]
    env = dict(
        os.environ,
        PYTHONPATH=':'.join(sys.path),
    )

    _LOG.debug('Executing fakeroot/create (cmd == %r, env == %r)...',
               cmd,
               env)
    sub_p = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        env=env,
    )

    try:
        # Send configuration.
        marshal.dump({
            'tree_path': tree_path,
        }, sub_p.stdin)

        # Send items.
        for item in items:
            marshal.dump(_simplify_item(item), sub_p.stdin)

        # Send "EOF".
        marshal.dump(None, sub_p.stdin)
    finally:
        sub_p.stdin.close()

    ret_code = sub_p.wait()
    _LOG.debug('fakeroot/create finished with code %d', ret_code)
    if ret_code:
        raise RuntimeError(
            'fakeroot/create returned error code {}'.format(ret_code))


def _squash_tree(fr_save_path, tree_path, destination):
    cmd = [
        _FAKEROOT,
        '-i',  # load fake environment from file
        fr_save_path,
        '--',
        _MKSQUASH,
        tree_path,
        destination,
    ]
    _LOG.info('Creating SquashFS...')
    _LOG.debug('Executing fakeroot/squash (cmd == %r)...', cmd)
    subprocess.check_call(cmd)
    _LOG.info('Done creating SquashFS: %s', destination)


def create_hole_tree_image(items, destination, tmp_dir):
    fr_save_path = os.path.join(tmp_dir, 's')
    tree_path = os.path.join(tmp_dir, 't')
    _create_tree(items, fr_save_path, tree_path)
    _squash_tree(fr_save_path, tree_path, destination)


if __name__ == "__main__":
    _create_tree_process()
