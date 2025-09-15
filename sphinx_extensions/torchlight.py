import re
from pygments.formatter import Formatter
from pygments.formatters.html import HtmlFormatter
from pygments.token import Token, Comment, Text

from sphinx.highlighting import PygmentsBridge
from sphinx.util import logging

logger = logging.getLogger(__name__)

class TorchlightHtmlFormatter(HtmlFormatter):
    def __init__(self, **options):
        options['linenos'] = 'inline'
        super().__init__(**options)
        self.options['nowrap'] = True # Ensure no extra wrapping by base class
        logger.debug("[torchlight] TorchlightHtmlFormatter __init__ called!")
        self.in_add_block = False
        self.in_remove_block = False

    def wrap(self, source):
        logger.debug("[torchlight] TorchlightHtmlFormatter wrap() method called!")
        # Call the parent's wrap method to get the default Pygments output
        for type, value in super().wrap(source):
            if type == 1: # This type typically indicates a line of code

                # Replace spaces inside and after the linenos span
                # e.g. <span class="linenos"> 1</span>  foo
                # -> <span class="linenos">&#160;1</span>&#160;&#160;foo

                # Handle spaces inside the linenos span, before the number
                value = re.sub(
                    r'(<span class="linenos">)( +)(\d+</span>)',
                    lambda m: m.group(1) + ''.join(['&#160;' for char in m.group(2)]) + m.group(3),
                    value
                )

                # Handle spaces after the linenos span
                value = re.sub(
                    r'(<span class="linenos">.*?</span>)( +)',
                    lambda m: m.group(1) + ''.join(['&#160;' for char in m.group(2)]),
                    value
                )

                # Handle spaces inside pygments' whitespace-only spans
                value = re.sub(
                    r'(<span class="w">)( +)(</span>)',
                    lambda m: m.group(1) + ''.join(['&#160;' for char in m.group(2)]) + m.group(3),
                    value
                )

                # Handle leading spaces in sd spans
                value = re.sub(
                    r'(<span class="sd">)( +)',
                    lambda m: m.group(1) + ''.join(['&#160;' for char in m.group(2)]),
                    value
                )

                

                # --- Wrap line and code in spans, as per user request ---
                # 1. Separate newline
                newline_suffix = ''
                if value.endswith('\n'):
                    value = value[:-1]
                    newline_suffix = '\n'

                # 2. Separate line number span from the rest of the code
                linenos_span = ''
                code_part = ''
                match = re.match(r'(<span class="linenos">.*?</span>)(.*)', value)
                if match:
                    linenos_span = match.group(1)
                    code_part = match.group(2)
                else:
                    # Fallback for lines without a line number
                    code_part = value

                # 3. Determine highlight class and clean tags from code_part
                line_highlight_class = None
                
                # Pattern to find [tl! add|remove] tags, accounting for Pygments' spans
                tag_pattern = r'(?P<prefix>//\s*)?\[tl!\s*(?P<type>add|remove)(?::(?P<subtype>start|end))?\]'
                
                tag_match = re.search(tag_pattern, code_part)
                
                if tag_match:
                    tag_type = tag_match.group('type')
                    tag_subtype = tag_match.group('subtype')
                    
                    logger.debug(f"[torchlight] Found tag: {tag_match.group(0)}. Type: {tag_type}, Subtype: {tag_subtype}")

                    if tag_type == 'add':
                        if tag_subtype is None:
                            line_highlight_class = "hll"
                        elif tag_subtype == 'start':
                            self.in_add_block = True
                            line_highlight_class = "hll"
                            logger.debug(f"[torchlight] Started add block.")
                        elif tag_subtype == 'end':
                            if self.in_add_block:
                                line_highlight_class = "hll"
                            self.in_add_block = False
                            logger.debug(f"[torchlight] Ended add block.")
                    
                    elif tag_type == 'remove':
                        if tag_subtype is None:
                            line_highlight_class = "dll"
                        elif tag_subtype == 'start':
                            self.in_remove_block = True
                            line_highlight_class = "dll"
                            logger.debug(f"[torchlight] Started remove block.")
                        elif tag_subtype == 'end':
                            if self.in_remove_block:
                                line_highlight_class = "dll"
                            self.in_remove_block = False
                            logger.debug(f"[torchlight] Ended remove block.")

                    # Remove the tag and clean up leftover spans
                    code_part = code_part.replace(tag_match.group(0), '')
                    code_part = re.sub(r'<span class="c[0-9]">\s*</span>', '', code_part)
                    logger.debug(f"[torchlight] Tag removed. Code part after removal: {code_part.strip()}")

                # Apply highlighting based on active block state
                elif self.in_add_block:
                    line_highlight_class = "hll"
                    logger.debug(f"[torchlight] Applying hll due to active add block.")
                elif self.in_remove_block:
                    line_highlight_class = "dll"
                    logger.debug(f"[torchlight] Applying dll due to active remove block.")

                # 4. Wrap the code part in its own span
                if not code_part.strip():
                    wrapped_code = '<span class="code empty">&#10;</span>'
                    # wrapped_code = '<span class="code empty"><svg xmlns="http://www.w3.org/2000/svg" width="8" height="8" viewBox="0 0 8 8" />&#10;</span>'
                else:
                    wrapped_code = f'<span class="code">{code_part}</span>'
                
                # 5. Assemble the new line structure with combined classes
                final_line_class = "line"
                if line_highlight_class:
                    final_line_class += f" {line_highlight_class}"
                
                value = f'<span class="{final_line_class}">{linenos_span}{wrapped_code}</span>'

                # 6. Add the newline back and yield
                value += newline_suffix
                yield type, value
            else:

                if value.strip() == '<pre><span></span>':
                    yield type, '<pre>\n'
                else:
                    yield type, value # Yield other types (e.g., 'doc') unchanged

def setup(app):
    logger.info("[torchlight] Torchlight Sphinx extension loaded!")

    # Directly modify the class attribute of PygmentsBridge
    # This ensures that any new PygmentsBridge instances will use our formatter
    PygmentsBridge.html_formatter = TorchlightHtmlFormatter

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }