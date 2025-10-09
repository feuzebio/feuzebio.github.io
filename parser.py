import re

def parse_code(code_str):
    """
    Parses the simplified UI description code and returns a list of component dictionaries.
    """
    components = []
    lines = code_str.strip().split('\n')

    # Regex to capture component type and properties string
    component_regex = re.compile(r"(\w+)\((.*)\)")
    # Regex to parse properties like key='value' or key=123
    props_regex = re.compile(r"(\w+)\s*=\s*('[^']*'|\"[^\"]*\"|[\d\.]+)")

    for line in lines:
        line = line.strip()
        if not line:
            continue

        match = component_regex.match(line)
        if not match:
            # Handle potential syntax errors gracefully
            print(f"Sintaxe inválida na linha: {line}")
            continue

        comp_type = match.group(1).lower()
        props_str = match.group(2)

        properties = {}
        prop_matches = props_regex.findall(props_str)

        for key, value in prop_matches:
            # Clean up the value: remove quotes for strings, convert numbers
            if value.startswith("'") and value.endswith("'"):
                properties[key] = value[1:-1]
            elif value.startswith('"') and value.endswith('"'):
                properties[key] = value[1:-1]
            else:
                try:
                    # Try converting to int, then float, else keep as string
                    if '.' in value:
                        properties[key] = float(value)
                    else:
                        properties[key] = int(value)
                except ValueError:
                    properties[key] = value # Should not happen with the regex, but for safety

        components.append({
            'tipo': comp_type,
            'propriedades': properties
        })

    return components