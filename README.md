# go-installer

The Base Application is generally for all Linux Systems, but the Makefile is created for Debian

# Create Debian Package

```bash
git clone https://github.com/pacflypy/go-installer
cd go-installer
make all_package
make clean
sudo dpkg -i go-installer_*_all.deb
```

# Install Directly
```bash
git clone https://github.com/pacflypy/go-installer
cd go-installer
make build
(sudo) make install
make clean
```

# Uninstalling

Generally you can use the Makefile for Uninstalling

```bash
(sudo) make remove
```

If you have install the .deb then use, for safe an Broken install

```bash
(sudo) apt remove go-installer
```


