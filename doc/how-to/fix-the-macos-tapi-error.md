# Fix `ld: tapi error: malformed file` on macOS

The host platforms link with Apple's `ld`, which comes from the developer directory that
`xcode-select -p` points to. When the Command Line Tools are newer than that Xcode, the SDK the
compiler picks has `.tbd` stubs the older `ld` cannot read:

```text
ld: tapi error: malformed file
.../MacOSX27.0.sdk/usr/lib/libSystem.B.tbd:4:20: error: unknown architecture
```

The project's `.env` sets `DEVELOPER_DIR=/Library/Developer/CommandLineTools`, so every
step of a pipeline run takes the linker and the SDK from the Command Line Tools, whatever
`xcode-select` says. Other platforms ignore the variable. Two consequences:

- The Command Line Tools must be installed (`xcode-select --install`); Xcode alone is not enough.
- A shell outside the pipeline gets the same setting from `.yanga/build/install/env_setup.sh`.

The `test` platform's gcc does not parse the SDK 26.x headers (`mach/message.h`); it works with SDK 15.x
and 27, and prefers a 15.x SDK from the Command Line Tools when one is installed.
