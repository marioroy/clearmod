# ClearMod

Run [XanMod](https://github.com/xanmod) Kernels on [Clear Linux](https://www.clearlinux.org) with ease.

The motivation comes from liking the XanMod kernel and opportunity to run a
preempt-enabled Linux kernel. The XanMod kernels are configured to run equally
well on all x86-64 CPUs with minimum support of x86-64-v3. Additionally, I
enable the NTFS3 file-system driver, and NTSync or WineSync module for fast
kernel-backed Wine. The Edge, Main, and RT variants include le9's patchset,
providing anon and clean file pages protection under memory pressure.

In March 2024, I added support to build Clear's native kernel with BORE, and
enable preemption.

## Preparation and configuration

Install build-essential bundles or prerequisites for building the kernel.
The `wget` command is used to fetch the source archive from the web.

```bash
sudo swupd bundle-add \
bc bison c-basic devpkg-gmp devpkg-elfutils devpkg-openssl flex \
kernel-install linux-firmware lz4 make package-utils wget xz
```

Enable `sched_autogroup_enabled`. The knob optimizes the scheduler to isolate
aggressive CPU burners (like build jobs) from desktop applications.
The `sched_rt_runtime_us` value is to mitigate jitter running a process with
real-time attributes, while background jobs consume many CPU cores.

```bash
sudo tee -a "/etc/clr-power-tweaks.conf" >/dev/null <<'EOF'
/proc/sys/kernel/sched_autogroup_enabled 1
/proc/sys/kernel/sched_rt_runtime_us 980000
EOF
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

During testing, the XanMod `preempt_rt` kernel works with NVIDIA graphics.
Set a system-wide environment variable to have the driver installer ignore
`PREEMPT_RT` presense.

```bash
sudo mkdir -p "/etc/environment.d"
sudo tee "/etc/environment.d/10-nvidia-ignore-rt.conf" >/dev/null <<'EOF'
IGNORE_PREEMPT_RT_PRESENCE=1
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

The default variants are apples-to-apples to Clear's flavors. Basically,
minimum overrides. The preempt variants enable `PREEMPT` or `PREEMPT_RT`.
The `clear` variants build the Clear native kernel.

Decide on the kernel to build. Choose "main-preempt" if unsure or desire
to install just one kernel with BORE and preemption enabled.

The `fetch-src` command (run first) fetches `*.src.rpm` and `*.tar.gz` from
Intel and XanMod, respectively. The optional release argument to `xm-install`
and `xm-uninstall` is described below.

```bash
./fetch-src all | clear | edge | main | lts | rt

./xm-build clear-default | clear-preempt
./xm-build edge-default | edge-preempt
./xm-build main-default | main-preempt
./xm-build lts-default | lts-preempt
./xm-build rt-preempt

./xm-install clear-default | clear-preempt [<release>]
./xm-install edge-default | edge-preempt [<release>]
./xm-install main-default | main-preempt [<release>]
./xm-install lts-default | lts-preempt [<release>]
./xm-install rt-preempt [<release>]

./xm-uninstall all | clear | edge | main | lts | rt
./xm-uninstall clear-default | clear-preempt [<release>]
./xm-uninstall edge-default | edge-preempt [<release>]
./xm-uninstall main-default | main-preempt [<release>]
./xm-uninstall lts-default | lts-preempt [<release>]
./xm-uninstall rt-preempt [<release>]

./xm-list-kernels
```

The following are the steps to fetch the stable sources, build, and
install the kernel.

```bash
./fetch-src main
./xm-build main-preempt
./xm-install main-preempt
sync
```

The default timer frequency is `HZ_800`, for fast interactivity and improved
smoothness. To override, define `HZ=value` to `1000`, `800`, `720`, `625`,
`500`, `300`, `250`, or `100`.

```text
HZ=625 ./xm-build main-preempt
```

To quickly build a trimmed Linux kernel, `LOCALMODCONFIG=1` will build only
the modules you have running. Therefore, make sure that all modules you will
ever need are loaded. Keyboard modules for the `cpio` package, CD-ROM/DVD and
EXFAT/NTFS3 filesystems, and NTSYNC or WINESYNC are added in the SPEC files.

```bash
./fetch-src edge
LOCALMODCONFIG=1 ./xm-build edge-preempt
./xm-install edge-preempt
sync
```

The `xm-list-kernels` command lists `xm*` kernels only. An asterisk indicates
the kernel is live or running. One may not install over it or uninstall.
Boot into another kernel before removal via `xm-uninstall`.

```bash
./xm-list-kernels 
XM boot-manager entries
  org.clearlinux.xmedge-preempt.6.8.1-162
* org.clearlinux.xmmain-preempt.6.6.22-162

XM installed packages (excluding dev,extra,license)
  linux-xmedge-preempt-6.8.1-162
* linux-xmmain-preempt-6.6.22-162
```

The `xm-install` and `xm-uninstall` commands accept an optional argument to
specify the release number. By default, `xm-install` installs the most recent
build. Omitting the 2nd argument, `xm-uninstall` removes all releases.
Though, skips the running kernel.

```bash
./xm-uninstall edge-preempt 162
Removing org.clearlinux.xmedge-preempt.6.8.1-162
```

## Epilogue

The Clear and XanMod Edge, Main, and LTS variants include the [BORE](https://github.com/firelzrd/bore-scheduler) (Burst-Oriented Response Enhancer) CPU Scheduler. For the RT variant, BORE is excluded since defaulting to `PREEMPT_RT` preemption. Define the `BORE` variable to include the patch and enable `PREEMPT` instead.

```text
BORE=1 ./xm-build rt-preempt
```

The `/boot` partition has limited space. So, no reason to install many kernels.
Build the one you want and enjoy the Clear or XanMod kernel. If changing your
mind later, remember to manage and uninstall any unused kernels. Important:
keep at least one Clear Linux kernel, installed with the OS or via `swupd`.

To limit the number of CPUs used by `rpmbuild`, override the `%_smp_mflags`
macro. Adjust the integer value to your liking.

```bash
echo "%_smp_mflags -j4" >> ~/.rpmmacros
```

## Caveat

Configuring PAM or security limits, allowing users to run commands with
real-time capabilities does not work on Clear Linux. A workaround is making
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
* [BORE (Burst-Oriented Response Enhancer) CPU Scheduler](https://github.com/firelzrd/bore-scheduler)
* [XanMod Linux kernel source code tree](https://github.com/xanmod/linux)
* [Testing various timer frequencies](https://gist.github.com/marioroy/f383f1e9f18498a251beb5c0a9f33dcf)
* [Latency testing - 4 million pings](https://gist.github.com/marioroy/5b36c9b650cb2af42e702922a8466d69)
* [Generic vs. Trimmed kernel build times](https://community.clearlinux.org/t/nvidia-and-xanmod-cl-updates/9299/15)

