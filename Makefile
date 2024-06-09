PACKAGE_NAME=go-installer
VERSION=1.0
SECTION=dev
PRIORITY=optional
ARCH=all
MAINTAINER=Kevin Alexander Krefting <kakrefting@gmail.com>
DESCRIPTION=Installer for Go
PREFIX=/usr/local
CURRENT_DIR=$(shell pwd)
SRC_ROOT=$(CURRENT_DIR)/script
SRC_INSTALL=$(SRC_ROOT)/install
SRC_REMOVE=$(SRC_ROOT)/remove
SIZE=$(shell du -s $(CURRENT_DIR) | cut -f1)
DEBIAN_BINARY=2.0

.PHONY: all generate struct build install package clean

all: generate struct build install package

generate:
	cd $(CURRENT_DIR)
	echo 'Package: $(PACKAGE_NAME)' > control
	echo 'Version: $(VERSION)' >> control
	echo 'Section: $(SECTION)' >> control
	echo 'Priority: $(PRIORITY)' >> control
	echo 'Architecture: $(ARCH)' >> control
	echo 'Installed-Size: $(SIZE)' >> control
	echo 'Depends: python3, curl' >> control
	echo 'Maintainer: $(MAINTAINER)' >> control
	echo 'Description: $(DESCRIPTION)' >> control
	echo '' >> control

struct:
	mkdir -p $(CURRENT_DIR)$(PREFIX)/bin

build:
	cd $(CURRENT_DIR)
	mkdir -p $(CURRENT_DIR)/build
	python3 -m zipapp --python '/usr/bin/env python3' --output $(CURRENT_DIR)/build/install-go --compress $(SRC_INSTALL)
	python3 -m zipapp --python '/usr/bin/env python3' --output $(CURRENT_DIR)/build/remove-go --compress $(SRC_REMOVE)

install:
	cd $(CURRENT_DIR)
	mv $(CURRENT_DIR)/build/install-go $(CURRENT_DIR)$(PREFIX)/bin/install-go
	mv $(CURRENT_DIR)/build/remove-go $(CURRENT_DIR)$(PREFIX)/bin/remove-go
	tar -cJf $(CURRENT_DIR)/data.tar.xz ./usr
	tar -cJf $(CURRENT_DIR)/control.tar.xz ./control
	echo $(DEBIAN_BINARY) > $(CURRENT_DIR)/debian-binary
	ar rcs $(CURRENT_DIR)/$(PACKAGE_NAME)_$(VERSION)_all.deb debian-binary control.tar.xz data.tar.xz

clean:
	rm -rf $(CURRENT_DIR)/build
	rm -rf $(CURRENT_DIR)/control
	rm -rf $(CURRENT_DIR)/data.tar.xz
	rm -rf $(CURRENT_DIR)/control.tar.xz
	rm -rf $(CURRENT_DIR)/debian-binary
	rm -rf $(CURRENT_DIR)/usr