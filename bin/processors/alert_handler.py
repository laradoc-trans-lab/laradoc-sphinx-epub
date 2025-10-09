
import re

def process_alerts(content: str) -> str:
    """
    Replaces GitHub-flavored alerts with custom formatted strings.
    """
    alerts = {
        r'\[!NOTE\]': '<img src="../_static/icons8-note-100.png" width="18" height="18" style="vertical-align: middle" /> **備註**<br />',
        r'\[!INFO\]': '<img src="../_static/icons8-info-100.png" width="18" height="18" style="vertical-align: middle" /> **訊息** <br />',
        r'\[!TIP\]': '<img src="../_static/icons8-tip-100.png" width="18" height="18" style="vertical-align: middle" /> **提示** <br />',
        r'\[!IMPORTANT\]': '<img src="../_static/icons8-important-100.png" width="18" height="18" style="vertical-align: middle" /> **重要** <br />',
        r'\[!WARNING\]': '<img src="../_static/icons8-warning-100.png" width="18" height="18" style="vertical-align: middle" /> **警告** <br />',
    }

    for pattern, replacement in alerts.items():
        content = re.sub(pattern, replacement, content)
    
    return content
