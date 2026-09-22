.PHONY: slides

npm-install:
	@cd slides && npm install

slides:
	@cd slides && npm run dev
