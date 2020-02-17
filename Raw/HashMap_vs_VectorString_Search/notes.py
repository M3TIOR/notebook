# Copyright (c) 2019 Ruby Allison Rose
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""# Hashmap vs Vector String Search Speed"""#?MD?

"""## Primer
This document highlights my notes on search access speed when fetching data
from Vectorized String Lists and Hash Maps in the C++ programming language
across several implementations and usage scenarios.

I hypothesize that the following implementations will show a speed reduction
in Hash Map usage over Vectorized String Lists when the accessor function has
no way to store and recall the hash values of the hash maps' items. This
theory is built upon the fact that every search execution in that scenario
must invoke the hashing function on the source string to arive at the desired
value. Complementary; when the accessor function can associate hashed keys
with their values for retrieval, there will be a considerable speed increase.
"""#?MD?

# First we need to generate some test data; What better way to do this than
# with the brilliance of hypothesis.works

from subprocess import run
from hypothesis import given
from hypothesis.strategies import lists, characters, integers
