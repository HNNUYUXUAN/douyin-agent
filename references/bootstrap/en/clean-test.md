# Clean-device test checklist

Starting condition: Windows x64 with only WorkBuddy and its browser extension; no user-installed Git, Conda, Python or FFmpeg. Do not transfer author configuration, caches or ASR results.

1. Send the [first request](first-run.md). Record OS/architecture, WorkBuddy version, actual shell and missing dependencies.
2. The host reads the repository, obtains an ordinary directory, verifies version and prepares dependencies or opens official installers. The user handles necessary OS/license/login/purchase steps.
3. Install with workbuddy mode and verify actual discovery in the current working folder.
4. Record extension, desktop bridge and actual Douyin page reading separately. Mark only the browser actually tested as passed.
5. Open Agent Plan pages/local .env for user configuration. doctor/onboard are local checks; real calls need separate evidence.
6. Acquire one short public video completely, present its concrete preview, run after authorization, review and finalize. Verify MD/JSON retention and user-original preservation.
7. Restart WorkBuddy and ask about the existing report in the same working folder. Verify reading after cleanup. Introduce a harmless blocker in a separate test workspace, such as missing key, and verify Wiki search, local-case storage and retrieval.
8. Use the [acceptance template](../../../docs/agent/examples/clean-device.json), with passed/blocked/unverified, actual timestamps and sanitized evidence. Send specific failures to maintainers rather than credentials or complete private logs.

Repository preparation cannot prove another device passed. Only actual device evidence can update WorkBuddy, browser, cloud and other-device status.
