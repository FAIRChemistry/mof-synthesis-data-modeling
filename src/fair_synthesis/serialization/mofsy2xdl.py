import argparse
import os

from fair_synthesis.conversion_config import (
    ConversionConfig,
    ConversionSource,
    get_artifact_path,
    get_repo_root,
    iter_sources_for_step,
)
from fair_synthesis.formatting.utils import load_json, save_string_as_file
from fair_synthesis.generated_apis.procedure_data_structure import SynthesisProcedure
from lxml import etree
from string import Template


def convert_mofsy_procedure_to_xdl_string(mofsy: SynthesisProcedure) -> str:
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
        tag = value.get('$xml_type') if isinstance(
            value, dict) and '$xml_type' in value else key

        if isinstance(value, dict):
            # Build attributes including support for $xml_append inside _/@
            # fields
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
                if subkey in {
                    '$xml_type',
                    '$xml_append',
                    '#text',
                    '#cdata',
                        '#comment'}:
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


def run_mofsy2xdl_for_source(
    repo_root: str,
    config: ConversionConfig,
    source: ConversionSource,
) -> bool:
    procedure_path = get_artifact_path(repo_root, config, source, "procedure")
    output_path = get_artifact_path(repo_root, config, source, "xdl")

    if not os.path.exists(procedure_path):
        print(f"Skipping XDL conversion for missing procedure file: {procedure_path}")
        return False

    xml = convert_mofsy_procedure_to_xdl_string(
        SynthesisProcedure.from_dict(load_json(procedure_path)))
    save_string_as_file(xml, output_path)
    return True


def mofsy2xdl(
    procedure_path: str | None = None,
    output_path: str | None = None,
    repo_root: str | None = None,
    config: ConversionConfig | None = None,
) -> bool:
    if procedure_path and output_path:
        if not os.path.exists(procedure_path):
            print(f"Skipping XDL conversion for missing procedure file: {procedure_path}")
            return False
        xml = convert_mofsy_procedure_to_xdl_string(
            SynthesisProcedure.from_dict(load_json(procedure_path)))
        save_string_as_file(xml, output_path)
        return True

    resolved_repo_root = repo_root or get_repo_root()
    resolved_config = config or load_json(os.path.join(resolved_repo_root, 'data', 'conversion_sources.json'))
    ran_any = False
    for source in iter_sources_for_step(resolved_config, "mofsy_to_xdl"):
        ran_any = run_mofsy2xdl_for_source(resolved_repo_root, resolved_config, source) or ran_any
    return ran_any


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convert MOFSY procedure files to XDL.")
    parser.add_argument("--procedure-path")
    parser.add_argument("--output-path")
    return parser


if __name__ == '__main__':
    args = _build_arg_parser().parse_args()
    mofsy2xdl(
        procedure_path=args.procedure_path,
        output_path=args.output_path,
    )
