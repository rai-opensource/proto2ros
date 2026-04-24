# Copyright (c) 2024 Robotics and AI Institute LLC dba RAI Institute. All rights reserved.

"""Unit tests for proto2ros.output.interfaces."""

from rosidl_adapter.parser import Field, MessageSpecification, Type

from proto2ros.output.interfaces import dump_message_specification


def _make_spec(pkg: str, msg: str, fields: list) -> MessageSpecification:
    return MessageSpecification(pkg, msg, fields, [])


def test_dump_strips_self_package_qualifier() -> None:
    """Same-package type references must not be fully qualified in .msg output.

    rosidl's type-description generator fails with KeyError when a package
    fully qualifies its own type references (e.g. ``proto2ros/Value`` inside
    a ``proto2ros`` package message).  The emitted line must use the bare
    type name instead.
    """
    fields = [Field(Type("proto2ros/Value[]"), "values")]
    spec = _make_spec("proto2ros", "List", fields)
    output = dump_message_specification(spec)
    assert "proto2ros/Value" not in output, (
        "self-package qualifier must be stripped from same-package field types"
    )
    assert "Value[] values" in output


def test_dump_preserves_cross_package_qualifier() -> None:
    """Cross-package type references must keep their fully qualified form."""
    fields = [Field(Type("builtin_interfaces/Time"), "stamp")]
    spec = _make_spec("my_msgs", "Header", fields)
    output = dump_message_specification(spec)
    assert "builtin_interfaces/Time stamp" in output


def test_dump_preserves_primitive_fields() -> None:
    """Messages with only primitive fields must be unaffected."""
    spec = _make_spec("my_msgs", "Counts", [])
    output = dump_message_specification(spec)
    assert isinstance(output, str)

