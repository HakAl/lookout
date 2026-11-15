# Source map

Original local guidance, written for SKILLS-003 on 2026-10-03. No external skill
workflow or implementation was copied. These references explain selected
representation hazards, not a requirement to adopt their formats.

- [RFC 8785, sections 3.1–3.2](https://www.rfc-editor.org/rfc/rfc8785): JCS has
  explicit number, string and property-ordering rules; it preserves Unicode
  string data rather than normalizing it. Parsing and serializing can change
  numeric spelling and precision. Consult only if relevant to the actual
  protocol; a project does not become a JCS protocol by using this skill.
- Target schema, serializer/parser documentation and actual consumer source
  decide local behavior. Resolve their versions during review; this package
  intentionally pins no SDK or wire-format version.

The companion Rust supplement contains Rust/Serde-specific details. This skill
follows representations between implementations rather than repeating those
language rules. Mutable project examples and ownership remain outside this
package, in the instance's own records.
