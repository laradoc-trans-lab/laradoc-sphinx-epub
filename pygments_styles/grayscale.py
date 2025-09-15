"""
    Simple black/white for E-INK readers.
"""

from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, \
     Operator, Generic
from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, \
     Number, Operator, Generic, Whitespace


__all__ = ['GrayscaleStyle']


class GrayscaleStyle(Style):

    name = 'grayscale'

    background_color = "#ffffff"
    highlight_color = '#EEEEEE'

    styles = {
        Whitespace:                "#ffffff",
        Comment:                   "italic #888888",
        Comment.Preproc:           "noitalic #555555",
        Comment.Special:           "noitalic bg:#FFFFFF",

        Keyword:                   "bold #555555",
        Keyword.Pseudo:            "nobold",
        Keyword.Type:              "nobold #444444",

        Operator:                  "#666666",
        Operator.Word:             "bold #555555",

        Name.Builtin:              "#555555",
        Name.Function:             "#333333",
        Name.Class:                "bold #666666",
        Name.Namespace:            "bold #666666",
        Name.Exception:            "#555555",
        Name.Variable:             "#777777",
        Name.Constant:             "#777777",
        Name.Label:                "bold #333333",
        Name.Entity:               "bold #777777",
        Name.Attribute:            "#666666",
        Name.Tag:                  "bold #333333",
        Name.Decorator:            "bold #555555",

        String:                    "#777777",
        String.Doc:                "italic",
        String.Interpol:           "italic #999999",
        String.Escape:             "bold #777777",
        String.Regex:              "#555555",
        String.Symbol:             "#666666",
        String.Other:              "#777777",
        Number:                    "#888888",

        Generic.Heading:           "bold #333333",
        Generic.Subheading:        "bold #555555",
        Generic.Deleted:           "#555555",
        Generic.Inserted:          "#777777",
        Generic.Error:             "#888888",
        Generic.Emph:              "italic",
        Generic.Strong:            "bold",
        Generic.EmphStrong:        "bold italic",
        Generic.Prompt:            "bold #7E7E7E",
        Generic.Output:            "#888888",
        Generic.Traceback:         "#666666",

        Error:                     "border:#888888"
    }
