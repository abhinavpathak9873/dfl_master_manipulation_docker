# Research notes

Research supports a concrete work packet; it does not define architecture by
itself.

Before adopting a ROS/vendor/model dependency, verify its current source,
version, license, platform support, and local behavior. Record those facts in
the packet or backend that uses it so they stay near the implementation.

The focused dependency, Isaac ROS, and CaP-X notes remain supporting evidence.
They do not override the toolbox principles or create architecture. Their useful
conclusions are:

- reuse upstream ROS/model implementations instead of wrapping them to rename
  calls;
- pin dependencies that are actually adopted;
- keep GPU/native dependencies inside the backend that needs them;
- provide small examples and focused fixtures;
- keep ROS and backend implementation paths directly inspectable.
