# ClearMod

Run the [XanMod Edge](https://github.com/xanmod) kernel on [Clear Linux](https://www.clearlinux.org) with ease.

The motivation comes from liking the Clear and XanMod Linux kernels and opportunity to run a preempt-enabled kernel with the [BORE](https://github.com/firelzrd/bore-scheduler) (Burst-Oriented Response Enhancer) CPU Scheduler. They run equally well on all x86-64 CPUs with minimum support of x86-64-v3.

The XanMod Edge flavor includes NTSync (for fast kernel-backed Wine) and le9's
patchset (providing anon and clean file pages protection under memory pressure).

In March 2024, I added support to build Clear's native kernel. Support for the
XanMod LTS, Main, and RT variants were removed.

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
Intel and XanMod, respectively. The optional release argument to `xm-install`
and `xm-uninstall` is described below.

```bash
./fetch-src all | clear | edge

./xm-build clear-default | clear-preempt
./xm-build edge-default | edge-preempt

./xm-install clear-default | clear-preempt [<release>]
./xm-install edge-default | edge-preempt [<release>]

./xm-uninstall all | clear | edge
./xm-uninstall clear-default | clear-preempt [<release>]
./xm-uninstall edge-default | edge-preempt [<release>]

./xm-list-kernels
```

The following are the steps to fetch the stable sources, build, and
install the kernel.

```bash
./fetch-src edge
./xm-build edge-preempt
./xm-install edge-preempt
sync
```

The default timer frequency is `HZ_1000` to be consistent with Clear Linux.
To override, define `HZ=value` to `1000`, `800`, `720`, `625`, `500`, `300`,
`250`, or `100`. A lower Hz value may decrease power consumption or fan
speed revving up and down less often.

```text
HZ=800 ./xm-build edge-preempt
```

To quickly build a trimmed Linux kernel, `LOCALMODCONFIG=1` will build only
the modules you have running. Therefore, make sure that all modules you will
ever need are loaded. Keyboard modules for the `cpio` package, CD-ROM/DVD and
EXFAT/NTFS3 filesystems, and NTSYNC are added in the SPEC files.

```bash
./fetch-src clear
LOCALMODCONFIG=1 ./xm-build clear-preempt
./xm-install clear-preempt
sync
```

The `xm-list-kernels` command lists `xm*` kernels only. An asterisk indicates
the kernel is live or running. One may not install over it or uninstall.
Boot into another kernel before removal via `xm-uninstall`.

```bash
./xm-list-kernels 
XM boot-manager entries
  org.clearlinux.xmclear-preempt.6.8.2-165
* org.clearlinux.xmedge-preempt.6.8.2-165

XM installed packages (excluding dev,extra,license)
  linux-xmclear-preempt-6.8.2-165
* linux-xmedge-preempt-6.8.2-165
```

The `xm-install` and `xm-uninstall` commands accept an optional argument to
specify the release number. By default, `xm-install` installs the most recent
build. Omitting the 2nd argument, `xm-uninstall` removes all releases.
Though, skips the running kernel.

```bash
./xm-uninstall clear-preempt 165
Removing org.clearlinux.xmclear-preempt.6.8.2-165
```

## Epilogue

The `/boot` partition has limited space. So, no reason to install many kernels.
Build the one you want and enjoy the Clear or XanMod kernel. If changing your
mind later, remember to manage and uninstall any unused kernels. Important:
keep at least one Clear Linux kernel, installed with the OS or via `swupd`.

To limit the number of CPUs used by `rpmbuild`, override the `%_smp_mflags`
macro. Adjust the integer value to your liking.

```bash
echo "%_smp_mflags -j4" >> ~/.rpmmacros
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
* [BORE (Burst-Oriented Response Enhancer) CPU Scheduler](https://github.com/firelzrd/bore-scheduler)
* [XanMod Linux kernel source code tree](https://github.com/xanmod/linux)
* [Testing various timer frequencies](https://gist.github.com/marioroy/f383f1e9f18498a251beb5c0a9f33dcf)
* [Latency testing - 4 million pings](https://gist.github.com/marioroy/5b36c9b650cb2af42e702922a8466d69)
* [Generic vs. Trimmed kernel build times](https://community.clearlinux.org/t/nvidia-and-xanmod-cl-updates/9299/15?u=marioroy)
* [Running four tasks concurrently](https://community.clearlinux.org/t/nvidia-and-xanmod-cl-updates/9299/28?u=marioroy)

