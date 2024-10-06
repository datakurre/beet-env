{ vscode-with-extensions
, vscode-extensions
, vscode-marketplace
, vscodium
, ruff
, lib
, enableVim ? false }:

vscode-with-extensions.override {
  vscode = vscodium;
  vscodeExtensions = [
    vscode-extensions.bbenoist.nix
    vscode-extensions.ms-pyright.pyright
    vscode-extensions.ms-python.python
    vscode-extensions.ms-vscode.makefile-tools
    (vscode-marketplace.charliermarsh.ruff.overrideAttrs (old: {
      postInstall = ''
        rm -f $out/share/vscode/extensions/charliermarsh.ruff/bundled/libs/bin/ruff
        ln -s ${ruff}/bin/ruff $out/share/vscode/extensions/charliermarsh.ruff/bundled/libs/bin/ruff
      '';
    }))
    vscode-marketplace.mcbeet.vscode-beet
    vscode-marketplace.minecraftcommands.syntax-mcfunction
    vscode-marketplace.spgoding.datapack-language-server
  ] ++ lib.optionals enableVim [ vscode-extensions.vscodevim.vim ];
}
