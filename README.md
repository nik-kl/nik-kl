## 🛡️ Coordinated vulnerability disclosure

I read the source code of open-source projects, look for security bugs, report them privately, and help maintainers fix them.

<!-- DISCLOSURES:START -->
![Reported](https://img.shields.io/badge/coordinated_disclosures-15-blueviolet?style=flat-square)
![Public](https://img.shields.io/badge/public_%2F_fixed-3-brightgreen?style=flat-square)
![Focus](https://img.shields.io/badge/focus-self--hosted_web_apps-informational?style=flat-square)

| Project | Vulnerability | Severity | Status | Reference |
| :-- | :-- | :-: | :-: | :-- |
| [AiDex](https://github.com/CSCSoftware/AiDex) | OS command injection <sub>CWE-78</sub> | ![High 7.8](https://img.shields.io/badge/High_7.8-orange?style=flat-square) | ![published](https://img.shields.io/badge/published_·_CVE_pending-blue?style=flat-square) | [Advisory ↗](https://github.com/advisories/GHSA-xwqr-wrm9-h3jx) |
| [FS PBX](https://github.com/nemerald-voip/fspbx) | Unauth file upload + caller-ID <sub>CWE-862/434</sub> | ![High](https://img.shields.io/badge/High-orange?style=flat-square) | ![fixed](https://img.shields.io/badge/fixed_·_credited-brightgreen?style=flat-square) | [Release 2.2.0 ↗](https://github.com/nemerald-voip/fspbx/releases) |
| [little-backup-box](https://github.com/outdoorbits/little-backup-box) | Unauth OS command injection <sub>CWE-78/306</sub> | ![Critical 9.8](https://img.shields.io/badge/Critical_9.8-red?style=flat-square) | ![fixed](https://img.shields.io/badge/fixed_·_advisory_pending-brightgreen?style=flat-square) | [Fix commit ↗](https://github.com/outdoorbits/little-backup-box/commit/2783a83) |

<sub>More reports are in coordinated disclosure right now. They show up here once a fix is out. Thanks to every maintainer who took the time to look into a report and ship a fix. 💚</sub>

🏡 More on how I work and what I hold to: **[0w30.uk/research ↗](https://0w30.uk/research)**
<!-- DISCLOSURES:END -->

<details>
<summary><b>How I report</b></summary>
<br>

- I report privately: through GitHub's private vulnerability reporting where it's enabled, otherwise by e-mail to the maintainers.
- I only test on my own local setups, never on other people's live systems.
- Every report comes with steps you can reproduce in a few minutes, and I offer a fix or test your patch if you like.
- I use AI tools to help me read code and write. Every finding is reproduced by me before I report it.
- You decide the timeline. I wait for a fix before anything goes public.

</details>

### 🤝 Maintainers

Found your project in the table, or want a second pair of eyes on your auth code? Open an issue on one of my repos or mail me at git@0w30.uk. I'm happy to help with fixes and test patches.

💡 **Tip:** turn on [private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/working-with-repository-security-advisories/configuring-private-vulnerability-reporting-for-a-repository) for your repo (Settings → Security). It gives researchers a private channel to reach you, and it only takes a minute.
