import re
url_pattern = re.compile(r'(?:git@|(?:https?|git)://(?:[^@]+@)?)github.com[:/](.*?)(?:\.git)?$')
