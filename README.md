# ClearMod

Run [XanMod](https://github.com/xanmod) Kernels on [Clear Linux](https://www.clearlinux.org) with ease.

The motivation for this project is that I like the XanMod kernel. It works reasonably
well on Clear Linux. I enabled the WineSync driver for fast kernel-backed Wine.

## Preparation and configuration

Install build-essential bundles or prerequisites for building the kernel.
The `wget` command is used to fetch the source archive from the web.

```bash
sudo swupd bundle-add \
bc bison c-basic devpkg-gmp devpkg-elfutils devpkg-openssl flex \
kernel-install linux-firmware lz4 make package-utils wget xz
```

Enable `sched_autogroup_enabled`. This option optimizes the scheduler to
isolate aggressive CPU burners (like build jobs) from desktop applications.
Optionally, skip this step for servers.

```bash
echo "/proc/sys/kernel/sched_autogroup_enabled 1" |\
sudo tee -a /etc/clr-power-tweaks.conf
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

To run a realtime kernel using NVIDIA graphics, the driver modules will not
build unless a variable is set. You may skip this step if not planning on
running the XanMod `preempt_rt` kernel.

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

./xm-build edge-custom | edge-default | edge-preempt
./xm-build lts-custom | lts-default | lts-preempt
./xm-build rt-custom | rt-default | rt-preempt | rt-preempt_rt

./xm-install edge-custom | edge-default | edge-preempt [<release>]
./xm-install lts-custom | lts-default | lts-preempt [<release>]
./xm-install rt-custom | rt-default | rt-preempt | rt-preempt_rt [<release>]

./xm-uninstall edge-custom | edge-default | edge-preempt [<release>]
./xm-uninstall lts-custom | lts-default | lts-preempt [<release>]
./xm-uninstall rt-custom | rt-default | rt-preempt | rt-preempt_rt [<release>]

./xm-list-kernels
```

For my desktop computer, I prefer the `rt-preempt` variant. This XanMod kernel
is fast and closest to running like a realtime kernel. The following are the
commands to fetch the RT sources, build the kernel, and most exciting of all,
installation.

```bash
./fetch-src rt
./xm-build rt-preempt
./xm-install rt-preempt
```

The XanMod 6.5 kernel with preempt enabled is another consideration. This one
too is fast including sustaining low latency.

```bash
./fetch-src edge
./xm-build edge-preempt
./xm-install edge-preempt
```

The `xm-list-kernels` command lists XanMod kernels only. An asterisk indicates
the kernel is live or running. One may not install over it or uninstall. Simply
boot into another kernel before removal via `xm-uninstall`.

```bash
./xm-list-kernels 
XanMod boot-manager entries
Password: 
* org.clearlinux.xmedge-preempt.6.5.5-101
  org.clearlinux.xmrt-preempt.6.1.54-101

XanMod packages, exluding dev,extra,license
* linux-xmedge-preempt-6.5.5-101
  linux-xmrt-preempt-6.1.54-101
```

The `xm-install` and `xm-uninstall` commands accept an optional argument to
specify the release number e.g. 101. By default, `xm-install` installs the most
recent build. Omitting the 2nd argument, the `xm-uninstall` command uninstalls
all releases for the specified variant e.g. rt-preempt.

```bash
./xm-uninstall rt-preempt 101
Removing org.clearlinux.xmrt-preempt.6.1.54-101
```

## Epilogue

The default variant is apples-to-apples to Clear's kernel. Basically, no overrides.
The preempt variant enables (`preempt` or `preempt_rt`) and `rcu_boost`. As described
above, the custom variant is your local copy and safe from `git pull`. It contains 
the same overrides as preempt, but disabled in the spec file.

The `/boot` partition has limited space. So, no reason to install many XanMod
kernels. Build the one you want and enjoy the XanMod kernel. If later changing
your mind, remember to manage and uninstall any unused XanMod kernels.

To limit the number of CPUs used by `rpmbuild`, override the `%_smp_mflags` macro.
Adjust the integer value to your liking.

```bash
echo "%_smp_mflags -j8" >> ~/.rpmmacros
```

