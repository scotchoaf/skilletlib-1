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
from .panos import PanosSkillet


class PanValidationSkillet(PanosSkillet):

    def get_snippets(self) -> List[PanosSnippet]:
        snippet_path_str = self.skillet_dict['snippet_path']
        snippet_path = Path(snippet_path_str)
        snippet_list = list()
        for snippet_def in self.snippet_stack:
            if 'cmd' not in snippet_def:
                snippet_def['cmd'] = 'validate'
            elif snippet_def['cmd'] == 'validate_xml':
                snippet_def = self.load_element(snippet_def, snippet_path)
            elif snippet_def['cmd'] == 'set':
                snippet_def = self.load_element(snippet_def, snippet_path)

            if 'severity' not in snippet_def:
                snippet_def['severity'] = 'low'

            snippet = PanosSnippet(snippet_def)
            snippet_list.append(snippet)

        return snippet_list
