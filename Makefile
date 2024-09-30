.PHONY: shell
shell:
	nix develop

.PHONY: vim-shell
vim-shell:
	nix develop .#with-vim

.PHONY: format
format:
	nix fmt flake.nix
