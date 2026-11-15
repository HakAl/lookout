# Source map and adaptation

Checked 2026-10-03. This is a short, locally rewritten review supplement inspired
by [leonardomso/rust-skills](https://github.com/leonardomso/rust-skills/tree/fd2a861ab0406a4ac536a55274d14ea6fd1ca9c9),
commit `fd2a861ab0406a4ac536a55274d14ea6fd1ca9c9`. Its MIT notice is retained in
`../LICENSE`. Only selected source files were captured and evaluated; this does
not certify the upstream catalog. No upstream installer or scripts are included.

Use the row relevant to a disputed claim, not every source on every review.
Read the target dependency's versioned source/docs when its version differs.

| Question | Primary source and constraint |
| --- | --- |
| Edition versus compiler/MSRV | [Edition Guide](https://doc.rust-lang.org/edition-guide/editions/index.html); [Cargo rust-version](https://doc.rust-lang.org/cargo/reference/rust-version.html). A crate opts into an edition; supported compiler versions are a separate promise. |
| Float identity and ordering | [f64 to_bits](https://doc.rust-lang.org/std/primitive.f64.html#method.to_bits), [total_cmp](https://doc.rust-lang.org/std/primitive.f64.html#method.total_cmp). Numeric equality merges signed zeros; NaNs have distinct encodings. Total ordering is not validation. |
| JSON field behavior | [Serde field attributes](https://serde.rs/field-attrs.html); [serde_json serializer source](https://docs.rs/serde_json/latest/src/serde_json/ser.rs.html). Verify actual formatter/features and non-finite handling against the locked version. |
| Async locks | [Tokio Mutex](https://docs.rs/tokio/latest/tokio/sync/struct.Mutex.html), consulted at 1.53.1. Async guards support awaits, particularly around shared I/O; ordinary mutexes are useful for short non-awaiting data operations. |
| Cancellation | [Tokio select cancellation safety](https://docs.rs/tokio/latest/tokio/macro.select.html#cancellation-safety). Inspect the individual operation and drop/restart behavior, not just the macro. |
| Async traits and dynamic dispatch | [Rust dyn compatibility](https://doc.rust-lang.org/reference/items/traits.html#dyn-compatibility); [trait-variant make](https://docs.rs/trait-variant/latest/trait_variant/attr.make.html), consulted at 0.1.3. The documented Send variant returns `impl Future + Send`; it does not box futures or make that method dyn-compatible. |
| Deduplication/order | [Vec dedup](https://doc.rust-lang.org/std/vec/struct.Vec.html#method.dedup); [HashSet](https://doc.rust-lang.org/std/collections/struct.HashSet.html). Preserve required order explicitly; consecutive dedup is not general dedup of unsorted input. |
| Unsafe boundary | [Rustonomicon safe/unsafe interaction](https://doc.rust-lang.org/nomicon/safe-unsafe-meaning.html). Invariants can depend on surrounding safe code; check the abstraction, not just the unsafe block. |

## Deliberate differences from upstream

- No category-level CRITICAL/HIGH ranking, compulsory crate choices, naming/style
  checklist, performance-first default, Cargo profile template or automatic fixes.
- Corrected the float-equality/bit-identity conflation and the claim that
  `trait-variant` provides boxed dynamic dispatch.
- Replaced absolute lock-across-await and clone-avoidance rules with checks of
  the resource/state invariant and ownership requirements.
- Serialization choices follow the consuming protocol; omitting empty fields is
  not a default. Optimization must retain ordering and exact-byte contracts.
- Added explicit version/edition separation, independent-oracle questions and
  read-only execution boundaries. No automatic update or external-service flow.

These sources support technical facts, not every local review judgment. The
workspace admission receipt records the exact files, behavioral cases and limits.
