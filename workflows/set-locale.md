---
description: Set the system locale to en_HK.UTF-8 and enable Chinese character support.
---

1. Uncomment necessary locales in `/etc/locale.gen`
// turbo
2. Run `sudo sed -i 's/^# *en_HK.UTF-8 UTF-8/en_HK.UTF-8 UTF-8/' /etc/locale.gen`
// turbo
3. Run `sudo sed -i 's/^# *zh_HK.UTF-8 UTF-8/zh_HK.UTF-8 UTF-8/' /etc/locale.gen`
// turbo
4. Run `sudo sed -i 's/^# *zh_CN.UTF-8 UTF-8/zh_CN.UTF-8 UTF-8/' /etc/locale.gen`
// turbo
5. Run `sudo sed -i 's/^# *zh_TW.UTF-8 UTF-8/zh_TW.UTF-8 UTF-8/' /etc/locale.gen`
// turbo
6. Generate the locales by running `sudo locale-gen`
// turbo
7. Set the system-wide default locale by running `sudo update-locale LANG=en_HK.UTF-8 LC_ALL=en_HK.UTF-8`
// turbo
8. Ensure environment variables are set in `/etc/environment` for all users by running:
 `sudo grep -q "LANG=en_HK.UTF-8" /etc/environment || echo "LANG=en_HK.UTF-8" | sudo tee -a /etc/environment`
// turbo
9. Set the `LC_ALL` environment variable in `/etc/environment` by running:
 `sudo grep -q "LC_ALL=en_HK.UTF-8" /etc/environment || echo "LC_ALL=en_HK.UTF-8" | sudo tee -a /etc/environment`
10. For `fish` users, create a persistent configuration by running:
 `mkdir -p ~/.config/fish/conf.d/ && echo 'set -gx LANG en_HK.UTF-8\nset -gx LC_ALL en_HK.UTF-8' > ~/.config/fish/conf.d/locale.fish`
11. Apply the changes in the current session: `source ~/.config/fish/conf.d/locale.fish` (if using fish) or `export LANG=en_HK.UTF-8 LC_ALL=en_HK.UTF-8`
