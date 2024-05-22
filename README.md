# ClearMod

Run the [XanMod](https://github.com/xanmod) kernel on [Clear Linux](https://www.clearlinux.org) with ease.

The motivation comes from liking the Clear and XanMod Linux kernels, and opportunity to run a preempt-enabled kernel patched with [BORE](https://github.com/firelzrd/bore-scheduler) (Burst-Oriented Response Enhancer) CPU Scheduler, or [ECHO](https://github.com/hamadmarri/ECHO-CPU-Scheduler) (Enhanced CPU Handling Orchestrator). The kernels are configured to run equally well on all x86-64 CPUs with minimum support of x86-64-v3.

All variants include the v4l2-loopback patch. The XanMod kernel includes also, NTSync for fast kernel-backed Wine.

```text
clear - Clear native kernel + preemption
bore  - XanMod kernel + preemption + BORE
echo  - XanMod kernel + preemption + ECHO
```

The `*-rt` variants include the Linux realtime patch set.

```text
clear-rt, bore-rt, and echo-rt
```

## Preparation and configuration

Install build-essential bundles or prerequisites for building the kernel.
The `wget` command is used to fetch the source archive from the web.

```bash
sudo swupd bundle-add \
bc bison c-basic devpkg-gmp devpkg-elfutils devpkg-openssl flex \
kernel-install linux-firmware lz4 make package-utils wget xz \
dkms hardware-uefi init-rdahead
```

The power tweaks service is how Clear Linux sets reasonable power management
defaults. For additional tweaking and response time consistency, copy the
sample file to the `/etc` folder, or merge the entries manually. This requires
the `clr-power` service, enabled by default.

```bash
sudo cp share/clr-power-tweaks.conf /etc/.
```

Do not tune or add `base_slice_ns` manually. Rather, let the kernel set the
value automatically. The value differs between EEVDF/BORE (high number) and
ECHO (low number).

```text
# /sys/kernel/debug/sched/base_slice_ns <value>
```

Set boot-timeout and system‐wide configuration to avoid `clr‐boot‐manager`
changing efi variables.

```bash
sudo mkdir -p "/etc/kernel"
sudo tee "/etc/kernel/timeout" >/dev/null <<'EOF'
5
EOF
sudo tee "/etc/kernel/update_efi_vars" >/dev/null <<'EOF'
false
EOF
```

## Clone the repository

The GitHub repo provides auto completion for the `bash` shell.

```bash
git clone https://github.com/marioroy/clearmod
cd clearmod

mkdir -p ~/.local/share/bash-completion/completions
cp -a share/bash-completion/completions/* \
   ~/.local/share/bash-completion/completions/
```

## Synopsis and simulation

The `fetch-src` command (run first) fetches `*.src.rpm` and `*.tar.gz` from
Clear and XanMod, respectively. The optional release argument to `xm-install`
and `xm-uninstall` is described below.

Note: Running a realtime kernel using NVIDIA graphics requires 550 minimally.
The 535 driver on RT may result in schedule/lock errors.

```bash
./fetch-src

./xm-build clear | bore | echo
./xm-build clear-rt | bore-rt | echo-rt

./xm-install clear | bore | echo [<release>]
./xm-install clear-rt | bore-rt | echo-rt [<release>]

./xm-uninstall all
./xm-uninstall clear | bore | echo [<release>]
./xm-uninstall clear-rt | bore-rt | echo-rt [<release>]

./xm-kernels - list kernels and packages
./xm-purge   - purge packages
```

The following are the steps to fetch the stable sources, build, and
install the kernel.

```bash
./fetch-src
./xm-build bore
./xm-install bore
sync
```

To quickly build a trimmed Linux kernel, `LOCALMODCONFIG=1` will build only
the modules you have running. Therefore, make sure that all modules you will
ever need are loaded. Keyboard modules for the `cpio` package, CD-ROM/DVD and
EXFAT/NTFS3 filesystems, and NTSYNC are added in the SPEC files.

The default timer frequency is `HZ_800`. To override, define `HZ=value` to
`100`, `250`, `300`, `500`, `625`, `800`, or `1000`. A lower Hz value
may decrease power consumption or fan speed revving up and down. A great Hz
value for the desktop environment is 800 or 1000.

```text
./fetch-src
LOCALMODCONFIG=1 HZ=800 ./xm-build clear
./xm-install clear
sync
```

The `xm-kernels` command lists `xm*` kernels only. An asterisk indicates
the kernel is live or running. One may not install over it or uninstall.
Boot into another kernel before removal via `xm-uninstall`.

```bash
./xm-kernels 
XM boot-manager entries
* org.clearlinux.xmbore.6.9.1-180
  org.clearlinux.xmclear.6.9.1-180

XM installed packages (excluding dev,extra,license)
* linux-xmbore-6.9.1-180
  linux-xmclear-6.9.1-180
```

The `xm-install` and `xm-uninstall` commands accept an optional argument to
specify the release number. By default, `xm-install` installs the most recent
build. Omitting the 2nd argument, `xm-uninstall` removes all releases.
Though, skips the running kernel.

```bash
./xm-uninstall clear 180
Removing org.clearlinux.xmclear.6.9.1-180
```

The `clr-boot-manager update` command may remove older kernel versions.
Run the purge script, periodically, to uninstall packages for xm-kernels
no longer present in `/lib/modules`.

```bash
./xm-purge
```

## Epilogue

The `/boot` partition has limited space. So, no reason to install many kernels.
Build the one you want and enjoy the Clear or XanMod kernel. If changing your
mind later, remember to manage and uninstall any unused kernels. Important:
Keep at least one Clear Linux kernel, installed with the OS or via `swupd`.

To limit the number of CPUs used by `rpmbuild`, override the `%_smp_mflags`
macro. Adjust the integer value to your liking.

```bash
echo "%_smp_mflags -j4" >> ~/.rpmmacros
```

You may add a `build` script at the top level, ignored by `git`.
Set execute bits `chmod +x build` and run `./build`.

```bash
#!/bin/bash
time LOCALMODCONFIG=1 HZ=800 ./xm-build bore
```

Configuring PAM or security limits, allowing users to run commands with
real-time capabilities, does not work on Clear Linux. A workaround is making
a copy of `chrt` and giving it `cap_sys_nice+ep` capabilities. The `+ep`
indicate the capability sets effective and permitted.

```bash
chrt -f 10 echo "Aloha!"
chrt: failed to set pid 0's policy: Operation not permitted

sudo mkdir -p /usr/local/bin
sudo cp -a /usr/bin/chrt /usr/local/bin/.
sudo setcap cap_sys_nice+ep /usr/local/bin/chrt

# The path /usr/local/bin is searched before /usr/bin in $PATH env.
chrt -f 10 echo "Aloha!"
Aloha!
```

## See also

* [Is chrt broken for normal users?](https://github.com/clearlinux/distribution/issues/2962)
* [Testing various timer frequencies](https://gist.github.com/marioroy/f383f1e9f18498a251beb5c0a9f33dcf)
* [Running four tasks concurrently](https://community.clearlinux.org/t/nvidia-and-xanmod-cl-updates/9299/28?u=marioroy)
* [Latency testing - 4 million pings](https://gist.github.com/marioroy/5b36c9b650cb2af42e702922a8466d69)
* [Generic vs. Trimmed kernel build times](https://community.clearlinux.org/t/nvidia-and-xanmod-cl-updates/9299/15?u=marioroy)

