# Research notes

Research supports a concrete work packet; it does not define architecture by
itself.

Before adopting a ROS/vendor/model dependency, verify its current source,
version, license, platform support, and local behavior. Record those facts in
the packet or backend that uses it so they stay near the implementation.

The previous broad dependency, Isaac ROS, and CaP-X audits were removed from the
active plan. Their useful conclusions are preserved in the accepted direction:

- reuse upstream ROS/model implementations instead of wrapping them to rename
  calls;
- pin dependencies that are actually adopted;
- keep GPU/native dependencies inside the backend that needs them;
- provide small examples and focused fixtures;
- keep ROS and backend implementation paths directly inspectable.
