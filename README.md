# ClearMod

Run [XanMod](https://github.com/xanmod) Kernels on [Clear Linux](https://www.clearlinux.org) with ease.

The motivation for this project is that I like the XanMod kernel and opportunity
to run a preempt-enabled Linux kernel. The XanMod kernels are configured to run
equally well on all x86-64 CPUs with minimum support of x86-64-v3. Additionally,
I enabled FQ-PIE packet scheduling, NTFS3 file-system driver, and the WineSync
module for fast kernel-backed Wine.

The XanMod Edge variants include the [BORE](https://github.com/firelzrd/bore-scheduler) (Burst-Oriented Response Enhancer) CPU Scheduler patch. You can turn it off by setting the `sysctl -w kernel.sched_bore=0` or adding an entry to `/etc/clr-power-tweaks.conf`.

## Preparation and configuration

Install build-essential bundles or prerequisites for building the kernel.
The `wget` command is used to fetch the source archive from the web.

```bash
sudo swupd bundle-add \
bc bison c-basic devpkg-gmp devpkg-elfutils devpkg-openssl flex \
kernel-install linux-firmware lz4 make package-utils wget xz
```

Tweak scheduler to resolve the [kernel stalling](https://github.com/xanmod/linux/issues/402) on Clear Linux.
The tweaks are compatible with Clear and XanMod kernels.

```bash
sudo tee -a "/etc/clr-power-tweaks.conf" >/dev/null <<'EOF'
/sys/kernel/debug/sched/latency_ns 12000000
/sys/kernel/debug/sched/min_granularity_ns 1500000
/sys/kernel/debug/sched/wakeup_granularity_ns 3000000
/sys/kernel/debug/sched/migration_cost_ns 500000
EOF
```

Important, enable `sched_autogroup_enabled`. This option optimizes the scheduler
to isolate aggressive CPU burners (like build jobs) from desktop applications.

```bash
sudo tee -a "/etc/clr-power-tweaks.conf" >/dev/null <<'EOF'
/proc/sys/kernel/sched_autogroup_enabled 1
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

From testing, the XanMod `preempt_rt` kernel works with NVIDIA graphics.
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

Decide on the XanMod kernel you wish to run. I captured metrics for the LTS
and RT variants. Please refer to [benchmark results](https://gist.github.com/marioroy/7a6384286f367e53758072962ad36c7f).

The `fetch-src` command (run first) fetches `*.src.rpm` and `*.tar.gz` from
Intel and XanMod, respectively. The optional release argument is described below.

```bash
./fetch-src all | edge | lts | rt

./xm-build edge-default | edge-preempt
./xm-build lts-default | lts-preempt
./xm-build rt-preempt

./xm-install edge-default | edge-preempt [<release>]
./xm-install lts-default | lts-preempt [<release>]
./xm-install rt-preempt [<release>]

./xm-uninstall edge-default | edge-preempt [<release>]
./xm-uninstall lts-default | lts-preempt [<release>]
./xm-uninstall rt-preempt [<release>]

./xm-list-kernels
```

I selected the lts-preempt variant for my desktop computer. The following are
the commands to fetch the LTS sources, build, and install the XanMod kernel.

```bash
./fetch-src lts
./xm-build lts-preempt
./xm-install lts-preempt
```

The XanMod 6.7 kernel with preempt enabled is another consideration,
including sustaining low latency.

```bash
./fetch-src edge
./xm-build edge-preempt
./xm-install edge-preempt
```

The `xm-list-kernels` command lists XanMod kernels only. An asterisk indicates
the kernel is live or running. One may not install over it or uninstall.
Boot into another kernel before removal via `xm-uninstall`.

```bash
./xm-list-kernels 
XanMod boot-manager entries
  org.clearlinux.xmedge-preempt.6.7.4-131
* org.clearlinux.xmlts-preempt.6.1.77-128

XanMod packages, exluding dev,extra,license
  linux-xmedge-preempt-6.7.4-131
* linux-xmlts-preempt-6.1.77-128
```

The `xm-install` and `xm-uninstall` commands accept an optional argument to
specify the release number. By default, `xm-install` installs the most recent
build. Omitting the 2nd argument, `xm-uninstall` removes all releases.
Though, skips the running kernel.

```bash
./xm-uninstall edge-preempt 131
Removing org.clearlinux.xmedge-preempt.6.7.4-131
```

## Epilogue

The default variants are apples-to-apples to Clear's kernels. Basically,
no overrides. The preempt variants enable (`preempt` or `preempt_rt`).

The `/boot` partition has limited space. So, no reason to install many XanMod
kernels. Build the one you want and enjoy the XanMod kernel. If changing your
mind later, remember to manage and uninstall any unused XanMod kernels.
Keep at least one Clear kernel installed on the system.

To limit the number of CPUs used by `rpmbuild`, override the `%_smp_mflags`
macro. Adjust the integer value to your liking.

```bash
echo "%_smp_mflags -j4" >> ~/.rpmmacros
```

