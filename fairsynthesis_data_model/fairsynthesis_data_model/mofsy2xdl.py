import os

from utils import load_json, save_string_as_file
from generated.procedure_data_structure import Procedure
from lxml import etree
from string import Template

def convert_mofsy_procedure_to_xdl_string(mofsy: Procedure) -> str:
    """
    Convert Mofsy procedure to XDL format, which is in XML.
    """
    # Convert the Mofsy to a dictionary
    xdl_dict = mofsy.to_dict()

    # Convert the dictionary to XML
    xdl_xml = dict_to_xml("XDL", xdl_dict)

    return xdl_xml


def dict_to_xml(root_tag, data):
    """Convert a dict to XML with support for $xml_type, @attr, _attr, $xml_append, text/cdata/comments."""

    def build_element(parent, key, value):
        # Determine tag name
        tag = value.get('$xml_type') if isinstance(value, dict) and '$xml_type' in value else key

        if isinstance(value, dict):
            # Build attributes including support for $xml_append inside _/@ fields
            attribs = {}
            for k, v in value.items():
                if k.startswith('@') or k.startswith('_'):
                    attr_name = k.lstrip('@_')
                    if isinstance(v, dict) and '$xml_append' in v:
                        template = Template(v['$xml_append'])
                        rendered = template.safe_substitute(v)
                        attribs[attr_name] = str(rendered)
                    else:
                        attribs[attr_name] = str(v)

            text = value.get('#text')
            cdata = value.get('#cdata')
            comment = value.get('#comment')

            elem = etree.SubElement(parent, tag, attrib=attribs)

            if comment:
                elem.append(etree.Comment(comment))
            if cdata:
                elem.text = etree.CDATA(cdata)
            elif text:
                elem.text = text.strip() if isinstance(text, str) else str(text)

            # Recursively handle children
            for subkey, subval in value.items():
                if subkey in {'$xml_type', '$xml_append', '#text', '#cdata', '#comment'}:
                    continue
                if subkey.startswith('@') or subkey.startswith('_'):
                    continue  # already handled as attribute
                if isinstance(subval, list):
                    for item in subval:
                        build_element(elem, subkey, item)
                else:
                    build_element(elem, subkey, subval)

        elif isinstance(value, list):
            for item in value:
                build_element(parent, key, item)

        else:
            elem = etree.SubElement(parent, tag)
            elem.text = str(value)

    # Build root
    root = etree.Element(root_tag)
    for key, val in data.items():
        build_element(root, key, val)
    return etree.tostring(root, pretty_print=True, encoding="unicode")

if __name__ == '__main__':
    current_file_dir = __file__.rsplit('/', 1)[0]

    # sciformation case
    mofsy_file_path = os.path.join(current_file_dir, '../..', 'data', 'MOCOF-1', 'generated', 'procedure_from_sciformation.json')
    xml = convert_mofsy_procedure_to_xdl_string(Procedure.from_dict(load_json(mofsy_file_path)))
    print("XML Result: " + xml)
    save_string_as_file(xml, os.path.join(current_file_dir, '../..', 'data', 'MOCOF-1', 'generated', 'xdl_from_sciformation.xml'))

    # excel MIL_2 case
    mil_2_file_path = os.path.join(current_file_dir, '../..', 'data', 'MIL-88B_101', 'generated', 'procedure_from_MIL_2.json')
    xml = convert_mofsy_procedure_to_xdl_string(Procedure.from_dict(load_json(mil_2_file_path)))
    print("XML Result: " + xml)
    save_string_as_file(xml, os.path.join(current_file_dir, '../..', 'data', 'MIL-88B_101', 'generated', 'xdl_from_MIL_2.xml'))