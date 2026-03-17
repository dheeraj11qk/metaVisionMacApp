TOPIC ?= a turtle exploring a magical pond
APP_SCHEME = meta_ai_app
APP_PROJECT = meta_ai_app.xcodeproj
DERIVED_DATA = $(HOME)/Library/Developer/Xcode/DerivedData
VENV = .venv/bin/python

.PHONY: video build-app open-app

## Run full pipeline: make video TOPIC="your topic here"
video: build-app open-app
	$(VENV) agent_ai/agent.py "$(TOPIC)"

## Build the macOS app via xcodebuild
build-app:
	@echo "[Make] Building macOS app..."
	xcodebuild -project $(APP_PROJECT) \
		-scheme $(APP_SCHEME) \
		-configuration Debug \
		-derivedDataPath $(DERIVED_DATA)/meta_ai_app_build \
		build | xcpretty || true
	@echo "[Make] Build done."

## Open/launch the built app
open-app:
	@echo "[Make] Launching macOS app..."
	@APP_PATH=$$(find $(DERIVED_DATA)/meta_ai_app_build -name "$(APP_SCHEME).app" -type d 2>/dev/null | head -1); \
	if [ -n "$$APP_PATH" ]; then \
		open "$$APP_PATH"; \
		echo "[Make] App launched: $$APP_PATH"; \
		sleep 5; \
	else \
		echo "[Make] App not found, trying default DerivedData..."; \
		open $$(find $(DERIVED_DATA) -name "$(APP_SCHEME).app" -type d 2>/dev/null | head -1); \
		sleep 5; \
	fi
