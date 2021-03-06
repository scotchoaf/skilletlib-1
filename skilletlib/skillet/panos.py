# Copyright (c) 2018, Palo Alto Networks
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# Authors: Adam Baumeister, Nathan Embery

from pathlib import Path
from typing import List

from skilletlib.snippet.panos import PanosSnippet
from .base import Skillet
from ..exceptions import SkilletLoaderException


class PanosSkillet(Skillet):

    def get_snippets(self) -> List[PanosSnippet]:
        snippet_path_str = self.skillet_dict['snippet_path']
        snippet_path = Path(snippet_path_str)
        snippet_list = list()
        for snippet_def in self.snippet_stack:
            if 'cmd' not in snippet_def or snippet_def['cmd'] == 'set':
                snippet_def = self.load_element(snippet_def, snippet_path)

            snippet = PanosSnippet(snippet_def)
            snippet_list.append(snippet)

        return snippet_list

    @staticmethod
    def load_element(snippet_def: dict, snippet_path: Path) -> dict:
        if 'element' not in snippet_def or snippet_def['element'] == '':
            if 'file' not in snippet_def:
                raise SkilletLoaderException(
                    'YAMLError: Could not parse metadata file for snippet %s' % snippet_def['name'])
            snippet_file = snippet_path.joinpath(snippet_def['file'])
            if snippet_file.exists():
                with snippet_file.open() as sf:
                    snippet_def['element'] = sf.read()
            else:
                raise SkilletLoaderException('Could not load "file" attribute!')

        return snippet_def

