# VirtualDJ MCP Skill

## Purpose

This skill helps control VirtualDJ locally through a Python MCP server that sends MIDI messages to a virtual MIDI port.

It is intended for simple DJ actions such as:

- play
- pause
- crossfade
- echo
- MIDI setup and testing

## What this skill does

This skill provides a small MCP server that:

1. runs locally on the same machine as VirtualDJ
2. opens a configured MIDI output port
3. sends MIDI Control Change messages
4. relies on VirtualDJ controller mappings to translate those messages into DJ actions

## When to use this skill

Use this skill when the user wants to:

- set up a local MCP server for VirtualDJ
- control VirtualDJ with AI through OpenClaw
- map a virtual MIDI device in VirtualDJ
- test MIDI connectivity on macOS or Windows
- add simple DJ controls before building more advanced features

## When not to use this skill

Do not use this skill when:

- the user wants direct audio analysis from the skill itself
- the user wants beatmatching based on live audio input
- the user wants support for DJ software other than VirtualDJ without adapting the mappings
- the user wants operating system automation outside the local Python script

## Assumptions

- VirtualDJ is installed locally
- Python is installed
- the user can install Python packages
- a virtual MIDI port is available
- OpenClaw is configured to launch local MCP servers

## Recommended project structure

```text
virtualdj-mcp/
├── .venv
├── virtualdj_mcp.py
├── README.md
└── SKILL.md