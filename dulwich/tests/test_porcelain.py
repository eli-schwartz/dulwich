# test_porcelain.py -- porcelain tests
# Copyright (C) 2013 Jelmer Vernooij <jelmer@samba.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; version 2
# of the License or (at your option) a later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.

"""Tests for dulwich.porcelain."""

from cStringIO import StringIO
import shutil
import tarfile
import tempfile

from dulwich.porcelain import (
    archive,
    )
from dulwich.repo import Repo
from dulwich.tests.utils import (
    make_object,
    make_commit,
    )
from dulwich.tests import (
    TestCase,
    )
from dulwich.tests.utils import (
    build_commit_graph,
    )


class ArchiveTests(TestCase):
    """Tests for the archive command."""

    def setUp(self):
        super(TestCase, self).setUp()
        repo_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, repo_dir)
        self.repo = Repo.init_bare(repo_dir)

    def test_simple(self):
        c1, c2, c3 = build_commit_graph(self.repo.object_store, [[1], [2, 1], [3, 1, 2]])
        self.repo.refs["refs/heads/master"] = c3.id
        out = StringIO()
        err = StringIO()
        archive(self.repo.path, "refs/heads/master", outstream=out, errstream=err)
        self.assertEquals("", err.getvalue())
        tf = tarfile.TarFile(fileobj=out)
        self.addCleanup(tf.close)
        self.assertEquals([], tf.getnames())
