# ClearMod

Run a custom kernel on [Clear Linux](https://www.clearlinux.org) with ease.

The motivation comes from wanting preempt-enabled kernels patched with [BORE](https://github.com/firelzrd/bore-scheduler) (Burst-Oriented Response Enhancer) CPU Scheduler.

The kernels are configured to run equally well on all x86-64 CPUs with
minimum support of x86-64-v3. They include the v4l2-loopback patch and
NTSync for fast kernel-backed Wine.

```text
bore - Clear 6.11.y native kernel + preemption + BORE
bore-rt - Same features, plus the Linux realtime patch set
```

## Preparation and configuration

The Clear kernel config [enables](https://github.com/clearlinux-pkgs/linux/commit/2918f672) ZSTD module compression, since 41850. Thus, installation requires CL 41850 (or later) to continue i.e. kmod, toolchain, and zstd updates.

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

Copy the NTSync udev rule.

```bash
sudo mkdir -p /etc/udev/rules.d
sudo cp share/99-ntsync.rules /etc/udev/rules.d/.
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

The `fetch-src` command (run first) fetches the source rpm and tar archive.

Running a realtime kernel using NVIDIA graphics requires 550 minimally.

```bash
./fetch-src

./xm-build bore | bore-rt
./xm-install bore | bore-rt [<rel>]
./xm-uninstall bore | bore-rt [<rel>]
./xm-uninstall all

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
`1000`, `800`, `600`, or `500`. A lower Hz value may decrease power consumption
or fan speed revving up and down. On a machine with more than 32 CPU threads,
select `800` or `600` for smoother game play.

The RT variants include the real-time patch set, useful for projects with
hard or soft deadlines.

```text
./fetch-src
LOCALMODCONFIG=1 HZ=1000 ./xm-build bore
LOCALMODCONFIG=1 HZ=1000 ./xm-build bore-rt

./xm-install bore
./xm-install bore-rt

sync
```

The `xm-kernels` command lists `xm*` kernels only. An asterisk indicates
the kernel is live or running. One may not install over it or uninstall.
Boot into another kernel before removal via `xm-uninstall`.

```bash
./xm-kernels 
XM boot-manager entries
* org.clearlinux.xmbore.6.11.11-210
  org.clearlinux.xmbore-rt.6.11.11-210

XM installed packages (excluding dev,extra,license)
* linux-xmbore-6.11.11-210
  linux-xmbore-rt-6.11.11-210
```

The `xm-install` and `xm-uninstall` commands accept an optional argument to
specify the release number. By default, `xm-install` installs the most recent
build. Omitting the 2nd argument, `xm-uninstall` removes all releases.
Though, skips the running kernel.

```bash
./xm-uninstall bore-rt 210
Removing org.clearlinux.xmbore-rt.6.11.11-210
```

The `clr-boot-manager update` command may remove older kernel versions.
Run the purge script, periodically, to uninstall packages for xm-kernels
no longer present in `/lib/modules`.

```bash
./xm-purge
```

## Epilogue

The `/boot` partition has limited space. So, no reason to install many kernels.
Build the one you want and enjoy the Clear kernel. If changing your mind later,
remember to manage and uninstall any unused kernels. Moreover, purge old files
found under the `./rpmbuild/RPMS/x86_64/` folder to free up storage space.

To limit the number of CPUs used by `rpmbuild`, override the `%_smp_mflags`
macro. Adjust the integer value to your liking.

```bash
echo "%_smp_mflags -j4" >> ~/.rpmmacros
```

You may add a `build` script at the top level, ignored by `git`.
Set execute bits `chmod +x build` and run `./build`.

```bash
#!/bin/bash
time LOCALMODCONFIG=1 HZ=1000 ./xm-build bore
```

Configuring PAM or security limits, allowing users to run commands with
real-time capabilities, does not work on Clear Linux. A workaround is making
a copy of `chrt` and giving it `cap_sys_nice+ep` capabilities. The `+ep`
indicate the capability sets effective and permitted.

```bash
chrt -f 1 echo "Aloha!"
chrt: failed to set pid 0's policy: Operation not permitted

sudo mkdir -p /usr/local/bin
sudo cp -a /usr/bin/chrt /usr/local/bin/.
sudo setcap cap_sys_nice+ep /usr/local/bin/chrt

# The path /usr/local/bin is searched before /usr/bin in $PATH env.
chrt -f 1 echo "Aloha!"
Aloha!
```

## See also

* [Is chrt broken for normal users?](https://github.com/clearlinux/distribution/issues/2962)
* [Testing various timer frequencies](https://gist.github.com/marioroy/f383f1e9f18498a251beb5c0a9f33dcf)
* [Running four tasks concurrently](https://community.clearlinux.org/t/nvidia-and-xanmod-cl-updates/9299/28?u=marioroy)
* [Generic vs. Trimmed kernel build times](https://community.clearlinux.org/t/nvidia-and-xanmod-cl-updates/9299/15?u=marioroy)

