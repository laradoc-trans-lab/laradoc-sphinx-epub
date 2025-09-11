import re
from pygments.formatter import Formatter
from pygments.formatters.html import HtmlFormatter
from pygments.token import Token, Comment, Text

from sphinx.highlighting import PygmentsBridge
from sphinx.util import logging

logger = logging.getLogger(__name__)

class TorchlightHtmlFormatter(HtmlFormatter):
    def __init__(self, **options):
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
                processed_value = value
                line_highlight_class = None
                
                # Pattern to find [tl! add|remove] tags, accounting for Pygments' spans
                # Modified to capture and remove the '//' prefix as well
                tag_pattern = r'(?P<prefix>//\s*)?\[tl!\s*(?P<type>add|remove)(?::(?P<subtype>start|end))?\]'
                
                tag_match = re.search(tag_pattern, processed_value)
                
                if tag_match:
                    tag_type = tag_match.group('type')
                    tag_subtype = tag_match.group('subtype')
                    
                    logger.debug(f"[torchlight] Found tag: {tag_match.group(0)}. Type: {tag_type}, Subtype: {tag_subtype}")
                    logger.debug(f"[torchlight] Before replacement (group 0): '{tag_match.group(0)}'")
                    logger.debug(f"[torchlight] Before replacement (processed_value): '{processed_value.strip()}'")

                    if tag_type == 'add':
                        # --- Handle 'add' tags ---
                        if tag_subtype is None:  # Single line tag
                            line_highlight_class = "hll"
                        elif tag_subtype == 'start':
                            self.in_add_block = True
                            line_highlight_class = "hll"  # Highlight the start line itself
                            logger.debug(f"[torchlight] Started add block.")
                        elif tag_subtype == 'end':
                            if self.in_add_block:  # Highlight the end line if a block was active
                                line_highlight_class = "hll"
                            self.in_add_block = False
                            logger.debug(f"[torchlight] Ended add block.")
                    
                    elif tag_type == 'remove':
                        # --- Handle 'remove' tags ---
                        if tag_subtype is None:  # Single line tag
                            line_highlight_class = "dll"
                        elif tag_subtype == 'start':
                            self.in_remove_block = True
                            line_highlight_class = "dll"
                            logger.debug(f"[torchlight] Started remove block.")
                        elif tag_subtype == 'end':
                            if self.in_remove_block:  # Highlight the end line if a block was active
                                line_highlight_class = "dll"
                            self.in_remove_block = False
                            logger.debug(f"[torchlight] Ended remove block.")

                    # --- Remove the [tl! ...] tag and its '//' prefix from the processed_value ---
                    # Replace the entire matched tag (including the optional '//' prefix) with an empty string
                    processed_value = processed_value.replace(tag_match.group(0), '')
                    
                    # Clean up any empty comment spans that might be left behind
                    # This regex is more specific to Pygments' empty comment spans
                    processed_value = re.sub(r'<span class="c[0-9]">\s*</span>', '', processed_value)
                    logger.debug(f"[torchlight] After replacement (processed_value): '{processed_value.strip()}'")
                    
                    # Keep these commented out for now, as they caused XHTML validation issues
                    # processed_value = re.sub(r'<span class="c[0-9]">\\s*</span>', '', processed_value)
                    # processed_value = re.sub(r'<--\s*-->', '', processed_value) # For HTML comments
                    
                    logger.debug(f"[torchlight] Tag removed. Processed value after removal: {processed_value.strip()}")
                
                # --- Apply highlighting based on current state (for ranges) ---
                elif self.in_add_block:
                    line_highlight_class = "hll"
                    logger.debug(f"[torchlight] Applying hll due to active add block.")
                elif self.in_remove_block:
                    line_highlight_class = "dll"
                    logger.debug(f"[torchlight] Applying dll due to active remove block.")

                # --- Apply highlighting and yield ---
                if line_highlight_class:
                    # The 'value' from super().wrap(source) already contains the newline.
                    # We need to remove the newline from processed_value before wrapping,
                    # and then add it back after the span.
                    if processed_value.endswith('\n'):
                        processed_value = processed_value[:-1]
                        newline_suffix = '\n'
                    else:
                        newline_suffix = ''

                    yield type, f'<span class="{line_highlight_class}">{processed_value}</span>{newline_suffix}'
                    logger.debug(f"[torchlight] Wrapped line with {line_highlight_class}. Final HTML: {processed_value.strip()}")
                else:
                    yield type, value # Yield original value (with newline) if no tag or no active block
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