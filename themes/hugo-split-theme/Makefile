SHELL = /bin/bash
.SHELLFLAGS = -e -o pipefail -c

.PHONY: hugo-server-example-site-with-image
hugo-server-example-site-with-image:
	hugo server --source tests/exampleSiteWithImage --themesDir=../../../

.PHONY: hugo-server-example-site-with-video
hugo-server-example-site-with-video:
	hugo server --source tests/exampleSiteWithVideo --themesDir=../../../

.PHONY: sitespeed-io-example-site-with-image-desktop-mode
sitespeed-io-example-site-with-image-desktop-mode:
	rm --recursive --force tests/exampleSiteWithImage/sitespeed-result
	docker compose --file tests/exampleSiteWithImage/docker-compose.desktop.yml up --exit-code-from sitespeed

.PHONY: sitespeed-io-example-site-with-image-mobile-mode
sitespeed-io-example-site-with-image-mobile-mode:
	rm --recursive --force tests/exampleSiteWithImage/sitespeed-result
	docker compose --file tests/exampleSiteWithImage/docker-compose.mobile.yml up --exit-code-from sitespeed

.PHONY: sitespeed-io-example-site-with-video-desktop-mode
sitespeed-io-example-site-with-video-desktop-mode:
	rm --recursive --force tests/exampleSiteWithVideo/sitespeed-result
	docker compose --file tests/exampleSiteWithVideo/docker-compose.desktop.yml up --exit-code-from sitespeed

.PHONY: sitespeed-io-example-site-with-video-mobile-mode
sitespeed-io-example-site-with-video-mobile-mode:
	rm --recursive --force tests/exampleSiteWithVideo/sitespeed-result
	docker compose --file tests/exampleSiteWithVideo/docker-compose.mobile.yml up --exit-code-from sitespeed
